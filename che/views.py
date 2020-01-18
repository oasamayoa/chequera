from django.db.models import Q, Count

from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render

from .models import Cheque
from registro.models import Banco, Cuenta, Provedor
from che.forms import ChequeForm
from bases.views import SinPrivilegios

from django.utils import timezone
from django.template.loader import get_template
from .utils import render_to_pdf, Render #created in step 4
from django.views.generic import TemplateView , CreateView , DetailView , UpdateView , DeleteView, View
import django_filters
from datetime import *

from .filter import ChequeFilter


class ChequeView(SinPrivilegios, generic.ListView):
    permission_required = "che.view_cheque"
    model = Cheque
    template_name = "che/cheque_list.html"
    context_object_name = "obj"

class ChequeNew(SinPrivilegios, generic.CreateView):
    permission_required = "che.add_cheque"
    model=Cheque
    template_name="che/cheque_form.html"
    context_object_name = "obj"
    form_class = ChequeForm
    success_url=reverse_lazy("che:cheque_list")

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class ChequeEdit(SinPrivilegios, generic.UpdateView):
    permission_required = "che.edit_cheque"
    model=Cheque
    template_name="che/cheque_form.html"
    context_object_name = "obj"
    form_class = ChequeForm
    success_url=reverse_lazy("che:cheque_list")

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

@login_required(login_url='/login/')
@permission_required('inv.change_marca', login_url='bases:sin_privilegios')
def Cheque_inactivar(request,id):
    cheque = Cheque.objects.filter(pk=id).first()

    if request.method=='POST':
        if cheque:
            cheque.estado = not cheque.estado
            cheque.save()
            return HttpResponse('ok')
        return HttpResponse('FAIL')

    return HttpResponse("FAIL")


class ChequeDetailView(SinPrivilegios, generic.DetailView):
    permission_required = "che.detail_cheque"
    redirect_field_name = 'redirect_to'
    template_name = 'che/detail_cheque.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'
    queryset = Cheque.objects.all()
    context_object_name = 'cheque'


def is_valid_queryparam(param):
    return param != '' and param is not None


def Bancofilter(request):
    qs = Cheque.objects.all()
    proveedor = Provedor.objects.all()
    institucion = Cuenta.objects.all()
    bancario = Banco.objects.all()
    no_cheque_query = request.GET.get('no_cheque_query')
    cantidad_query = request.GET.get('cantidad_query')
    fecha_pagar_query = request.GET.get('fecha_pagar_query')
    no_fac_query = request.GET.get('no_fac_query')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    imagen_query = request.GET.get('imagen_query')
    cuenta_query = request.GET.get('cuenta_query')
    category = request.GET.get('category')
    categoria = request.GET.get('categoria')
    print(categoria)
    banco_query = request.GET.get('banco_query')


    if is_valid_queryparam(no_cheque_query):
            qs = qs.filter(no_cheque__icontains=no_cheque_query)

    if is_valid_queryparam(cantidad_query):
        qs = qs.filter(cantidad__icontains=cantidad_query)


    if is_valid_queryparam(fecha_pagar_query):
        qs = qs.filter(fecha_pagar__lt=fecha_pagar_query)

    if is_valid_queryparam(no_fac_query):
        qs = qs.filter(no_fac__icontains=no_fac_query)

    if is_valid_queryparam(date_min):
        qs = qs.filter(fecha_creado__gte=date_min)

    if is_valid_queryparam(date_max):
        qs = qs.filter(fecha_creado__lt=date_max)

    if is_valid_queryparam(category) and category != 'Choose...':
        qs = qs.filter(proveedor__nombre=category)

    if is_valid_queryparam(categoria) and categoria != 'Choose...':
        qs = qs.filter(cuenta__nombre=categoria)


    if is_valid_queryparam(imagen_query):
        qs = qs.filter(imagen__icontains=imagen_query)

    if is_valid_queryparam(cuenta_query):
        qs = qs.filter(cuenta__icontains=cuenta_query)


    return qs


@login_required(login_url='/login/')
@permission_required('che.change_marca', login_url='bases:sin_privilegios')
def BancoFilterView(request):
    qs = Bancofilter(request)
    context = {
        'queryset': qs,
        'proveedor': Provedor.objects.all(),
        'institucion': Cuenta.objects.all()
    }
    return render(request, "che/search_banco.html", context)

@login_required(login_url='/login/')
@permission_required('che.change_marca', login_url='bases:sin_privilegios')
def ProveedorFilterView(request):
    qs = Bancofilter(request)
    context = {
        'queryset': qs,
        'proveedor': Provedor.objects.all(),
        'institucion': Cuenta.objects.all()
    }
    return render(request, "che/search_proveedor.html", context)

@login_required(login_url='/login/')
@permission_required('che.change_marca', login_url='bases:sin_privilegios')
def filter(request):
    query1 = request.GET.get('q', '')
    query2 = request.GET.get('p', 'p')
    if query1:
        if query2:
            inicio = datetime.strptime(query1, '%Y-%m-%d')
            final = datetime.strptime(query2, '%Y-%m-%d')
            cheque = Cheque.objects.filter(fecha_creado__range =[inicio , final]).order_by('-fecha_creado')
        else :
            cheque = []
            inicio = []
    else :
        final = []
        cheque = []

    return render(request , 'che/che_form.html' , {'query1': query1 , 'query2' : query2 ,'cheque': cheque})

class ChequeGeneratePDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('che/cheque_print_all.html')
        cheque = Cheque.objects.all()
        params = {
            "cheque": cheque,


        }
        html = template.render(params)
        pdf = Render.render('che/cheque_print_all.html', params)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
