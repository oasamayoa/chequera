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
from .forms import ChequeForm
from bases.views import SinPrivilegios

from django.utils import timezone
from django.template.loader import get_template
from .utils import render_to_pdf, Render #created in step 4
from django.views.generic import TemplateView , CreateView , DetailView , UpdateView , DeleteView, View
import django_filters
from datetime import *

from .filter import ChequeFilter

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
        today = timezone.now()
        params = {
            "cheque": cheque,
            "today": today,
            # "titulo": "BENEMÉRITO CUERPO VOLUNTARIO DE BOMBEROS DE GUATEMALA",
            # "subtitulo": "REPORTE DE SERVICIOS VARIOS",

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
#
# @login_required(login_url='/login/')
# @permission_required('inv.change_marca', login_url='bases:sin_privilegios')
# def proveedor_inactivar(request,id):
#     template_name='registro/inactivar_pro.html'
#     contexto={}
#     pro = Provedor.objects.filter(pk=id).first()
#
#     if not pro:
#         return HttpResponse('Proveedor no existe ' + str(id))
#
#     if request.method=='GET':
#         contexto={'obj':pro}
#
#     if request.method=='POST':
#         pro.estado=False
#         pro.save()
#         contexto={'obj':'OK'}
#         return HttpResponse('Proveedor Inactivado')
#
#     return render(request,template_name,contexto)


class ChequeDetailView(SinPrivilegios, generic.DetailView):
    permission_required = "che.detail_cheque"
    redirect_field_name = 'redirect_to'
    template_name = 'che/detail_cheque.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'
    queryset = Cheque.objects.all()
    context_object_name = 'cheque'

@login_required(login_url='/login/')
@permission_required('che.change_marca', login_url='bases:sin_privilegios')
def filter_banco(request):
    q = Cuenta.objects.all()
    query1 = request.GET.get('q', '')
    query2 = request.GET.get('p', 'p')
    cuenta = request.GET.get('cuenta', '')
    if query1:

        if cuenta:
            q = (
                Q(cuenta__icontain=cuenta)
                )

        if query2:
            inicio = datetime.strptime(query1, '%Y-%m-%d')
            final = datetime.strptime(query2, '%Y-%m-%d')

            cheque = Cheque.objects.filter(fecha_creado__range =[inicio , final]).order_by('-fecha_creado')
        else :
            cheque = []
            inicio = []
            cuenta = []
    else :
        final = []
        cheque = []
        cuenta = []


    return render(request , 'che/search_banco.html' , {'query1': query1 , 'query2' : query2 , 'cheque': cheque})
