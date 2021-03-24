from django.db.models import Q, Count, Sum
from easy_pdf.views import PDFTemplateView, PDFTemplateResponseMixin
from django.views.decorators.csrf  import csrf_exempt


from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from django.core import serializers
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.shortcuts import render

from .models import Cheque, Deposito, Fisico_Entregado, Cheque_rechazado, Factura, Abono_Factura
from registro.models import Banco, Cuenta, Provedor
from che.forms import ChequeForm, DepositoForm, CheEntregadoForm, CheRechazadoForm, FacturaForm, AbonoForm, ChequeEditform
from bases.views import SinPrivilegios

from django.utils import timezone
from django.template.loader import get_template
from .utils import render_to_pdf, Render #created in step 4
from django.views.generic import TemplateView , CreateView , DetailView , UpdateView , DeleteView, View
import django_filters
from django.utils.dateparse import parse_date
from datetime import date, timedelta, datetime
from xhtml2pdf import pisa
import os
from django.conf import settings
from django.contrib.staticfiles import finders



from .filter import ChequeFilter


class ChequeView(SuccessMessageMixin,SinPrivilegios, generic.ListView):
    permission_required = "che.view_cheque"
    model = Cheque
    template_name = "che/cheque_list.html"
    # paginate_by = 10 esta opcion sirve para cuantos elementos queres mostrar por pagina


    def get_queryset(self):
        return self.model.objects.all().order_by('-fc')[:100]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DepositoView(SuccessMessageMixin,SinPrivilegios, generic.ListView):
    permission_required = "che.view_deposito"
    model = Deposito
    template_name = "che/deposito_list.html"



    def get_queryset(self):
        return self.model.objects.all().order_by('-fecha_creado')[:100]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class FacturaView(SuccessMessageMixin,SinPrivilegios, generic.ListView):
    permission_required = "che.view_factura"
    model = Factura
    template_name = "che/factura_list.html"



    def get_queryset(self):
        return self.model.objects.all().order_by('-fc')[:100]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class Abono_FacturaView(SuccessMessageMixin,SinPrivilegios, generic.ListView):
    permission_required = "che.view_factura"
    model = Abono_Factura
    template_name = "che/abono_factura_list.html"


    # def get_queryset(self):
    #     return self.model.objects.all().order_by('-fc')[:100]
    def get_queryset(self):
        try:
            if self.model.objects.latest('fc'):
                return self.model.objects.latest('fc')
        except self.model.DoesNotExist:
            abono = None




    # def get_queryset(self):
        # return  self.model.objects.latest('fc')


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context

class ChequeNew(SuccessMessageMixin,SinPrivilegios, generic.CreateView):
    permission_required = "che.add_cheque"
    model=Cheque
    template_name="che/cheque_form.html"
    context_object_name = "obj"
    form_class = ChequeForm
    success_url=reverse_lazy("che:cheque_list")

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


    # def post(self, request, *args, **kwargs):
    #     if request.is_ajax() and request.method == 'POST':
    #         form = ChequeForm(request.POST, request.FILES)
    #         form.instance.uc = self.request.user
    #         errores =  ''
    #         exito = False
    #         if form.is_valid():
    #             form.save()
    #             exito =  True
    #         else:
    #             errores = form.errors
    #         response = {exito:'exito', 'errores': errores}
    #         return HttpResponse(json.dumps(response))
    #     else:
    #         return JsonResponse({"error": ""}, status=400)


    # def post(self, request, *args, **kwargs):
    #     if self.request.is_ajax() and request.method == 'POST':
    #         form = ChequeForm(request.POST, request.FILES)
    #         form.instance.uc = self.request.user
    #         errores = ""
    #         if form.is_valid():
    #             form.save()
    #         else:
    #             errores = form.errors
    #             return HttpResponse(json.dumps(response), mimetype="application/json")
    #     else:
    #         return JsonResponse(form.errors, status=400)

    #
    # def form_invalid(self, form, request):
    #     response = super().form_invalid(form)
    #     if self.request.is_ajax() and request.method == 'POST':
    #         form = ChequeForm(request.POST, request.FILES)
    #         form.save()
    #         return JsonResponse(form.errors, status=400)
    #     else:
    #         return response


class DepositoNew(SuccessMessageMixin,SinPrivilegios, generic.CreateView):
    permission_required = "che.add_deposito"
    model=Deposito
    template_name="che/depo_form.html"
    context_object_name = "obj"
    form_class = DepositoForm
    success_url=reverse_lazy("che:deposito_list")

    def post(self, request, *args, **kwargs):
        form = DepositoForm(request.POST, request.FILES)
        if form.is_valid():
            self.object = form.save(commit=False)
            form.instance.uc = self.request.user
            id_che = self.object.cheque.pk
            cheque_update = Cheque.objects.get(pk=id_che)
            cheque_update.estado_che = True
            form.save()
            cheque_update.save()
            return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, {'form': form})

    # def form_valid(self, form):
    #     form.instance.uc = self.request.user
    #     return super().form_valid(form)

class FacturaNew(SuccessMessageMixin,SinPrivilegios, generic.CreateView):
    permission_required = "che.add_cheque"
    model=Factura
    template_name="che/factura_form.html"
    context_object_name = "obj"
    form_class = FacturaForm
    success_url=reverse_lazy("che:factura_list")

    # def post(self,  request, *args, **kwargs):
    #     form = FacturaForm(request.POST)
    #     if form.is_valid():
    #
    #
    #         form.save()
    #         factura.save()
    #     return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ChequeEdit(SuccessMessageMixin,SinPrivilegios, generic.UpdateView):
    permission_required = "che.change_cheque"
    model=Cheque
    template_name="che/cheque_form_edit.html"
    context_object_name = "obj"
    form_class = ChequeEditform
    success_url=reverse_lazy("che:cheque_list")

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

class DepositoEdit(SuccessMessageMixin,SinPrivilegios, generic.UpdateView):
    permission_required = "che.change_deposito"
    model=Deposito
    template_name="che/depo_form.html"
    context_object_name = "obj"
    form_class = DepositoForm
    success_url=reverse_lazy("che:deposito_list")

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

class FacturaEdit(SuccessMessageMixin,SinPrivilegios, generic.UpdateView):
    permission_required = "che.change_deposito"
    model=Factura
    template_name="che/factura_form.html"
    context_object_name = "obj"
    form_class = FacturaForm
    success_url=reverse_lazy("che:factura_list")

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

@login_required(login_url='/login/')
@permission_required('che.change_cheque', login_url='bases:sin_privilegios')
def Cheque_inactivar(request,id):
    cheque = Cheque.objects.filter(pk=id).first()

    if request.method=='POST':
        if cheque:
            cheque.estado = not cheque.estado
            cheque.save()
            return HttpResponse('ok')
        return HttpResponse('FAIL')

    return HttpResponse("FAIL")


class ChequeDetailView(SuccessMessageMixin,SinPrivilegios, generic.DetailView):
    permission_required = "che.change_cheque"
    redirect_field_name = 'redirect_to'
    template_name = 'che/detail_cheque.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'
    queryset = Cheque.objects.all()
    context_object_name = 'cheque'

class DepositoDetailView(SuccessMessageMixin,SinPrivilegios, generic.DetailView):
    permission_required = "che.change_deposito"
    redirect_field_name = 'redirect_to'
    template_name = 'che/detail_deposito.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'
    queryset = Deposito.objects.all()
    context_object_name = 'deposito'


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
@permission_required('che.change_cheque', login_url='bases:sin_privilegios')
def BancoFilterView(request):
    # qs = Bancofilter(request)
    value = request.GET.get('date_min' , '')
    if value:
        qs = Bancofilter(request)
    else:
        qs = {}
    context = {
        'queryset': qs,
        'proveedor': Provedor.objects.all(),
        'institucion': Cuenta.objects.all()
    }
    return render(request, "che/search_banco.html", context)

@login_required(login_url='/login/')
@permission_required('che.change_cheque', login_url='bases:sin_privilegios')
def ProveedorFilterView(request):
    # qs = Bancofilter(request)
    value = request.GET.get('date_min' , '')
    if value:
        qs = Bancofilter(request)
    else:
        qs = {}
    context = {
        'queryset': qs,
        'proveedor': Provedor.objects.all(),
        'institucion': Cuenta.objects.all()
    }
    return render(request, "che/search_proveedor.html", context)

@login_required(login_url='/login/')
@permission_required('che.change_cheque', login_url='bases:sin_privilegios')
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
        pdf = Render.render('', params)
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

@login_required(login_url='/login/')
@permission_required('che.change_cheque', login_url='bases:sin_privilegios')
def imprimir_cheque_list(request, f1,f2):
    template_name = "che/cheque_print_all.html"
    f1=parse_date(f1)
    f2=parse_date(f2)
    enc = Cheque.objects.filter(fecha_creado__range = [f1 , f2]).order_by('-fecha_creado')
    suma = 0
    for cheque in enc:
        suma = suma+cheque.cantidad
    context = {
        'request': request,
        'f1':f1,
        'f2':f2,
        'enc':enc,
        'suma':suma
    }
    return render(request, template_name, context)

@login_required(login_url='/login/')
@permission_required('che.change_deposito', login_url='bases:sin_privilegios')
def imprimir_deposito_list(request, f1,f2):
    template_name = "che/deposito_print_all.html"
    f1=parse_date(f1)
    f2=parse_date(f2)
    enc = Deposito.objects.filter(fecha_creado__range = [f1 , f2]).order_by('-fecha_creado')
    suma = 0
    for deposito in enc:
        suma = suma+deposito.cantidad
    context = {
        'request': request,
        'f1':f1,
        'f2':f2,
        'enc':enc,
        'suma':suma
    }
    return render(request, template_name, context)

@login_required(login_url='/login/')
@permission_required('che.change_cheque', login_url='bases:sin_privilegios')
def imprimir_cheque_img(request, f1,f2):
    template_name = "che/cheque_print_img.html"
    f1=parse_date(f1)
    f2=parse_date(f2)
    enc = Cheque.objects.filter(fecha_creado__range = [f1 , f2]).order_by('-fecha_creado')
    suma = 0
    for cheque in enc:
        suma = suma+cheque.cantidad
    context = {
        'request': request,
        'f1':f1,
        'f2':f2,
        'enc':enc,
        'suma':suma
    }
    return render(request, template_name, context)


@login_required(login_url='/login/')
@permission_required('che.change_cheque', login_url='bases:sin_privilegios')
def Vista_Proveedor(request):
    categoria = Provedor.objects.all()
    results = Cheque.objects.all()
    template_name = "che/cheque_vista_pdf.html"

    context = {
        'categoria': Provedor.objects.all(),
        'results': Cheque.objects.all()
    }

    return render(request, template_name, context)


@login_required(login_url='/login/')
@permission_required('che.change_cheque', login_url='bases:sin_privilegios')
def imprimir_provedor(request,f5,f6 , categoria):
    template_name = "che/cheque_print_prove.html"
    f5=parse_date(f5)
    f6=parse_date(f6)
    prueba = []
    pro = []
    query = []
    enc = Cheque.objects.filter(fecha_creado__range =  [f5, f6] , proveedor=categoria).order_by('-fecha_creado')
    suma = 0
    for cheque in enc:
        suma = suma+cheque.cantidad

    return render(request, template_name, {'f5':f5,'f6':f6, 'categoria': categoria,'prueba':prueba,'query':query, 'enc':enc, 'pro':pro, 'suma':suma})

@login_required(login_url='/login/')
@permission_required('che.change_cheque', login_url='bases:sin_privilegios')
def Vista_Banco(request):
    categoria = Cuenta.objects.all()
    cheque = Cheque.objects.all()
    template_name = "che/cheque_vista_bancopdf.html"

    context = {
        'categoria': Cuenta.objects.all(),
        'cheque':  Cheque.objects.all()
    }

    return render(request, template_name, context)

@login_required(login_url='/login/')
@permission_required('che.change_cheque', login_url='bases:sin_privilegios')
def imprimir_banco(request,f5,f6 , categoria):
    template_name = "che/cheque_print_banco.html"
    f5=parse_date(f5)
    f6=parse_date(f6)
    prueba = []
    pro = []
    query = []
    enc = Cheque.objects.filter(fecha_creado__range =  [f5, f6] , cuenta__nombre=categoria).order_by('-fecha_creado')

    #tot = Cheque.objects.filter(fecha_creado__range = [f5, f6], cuenta__nombre=categoria).aggregate(Sum('cantidad'))
    suma = 0
    for cheque in enc:
        suma = suma+cheque.cantidad
    return render(request, template_name, {'f5':f5,'f6':f6, 'categoria': categoria,'prueba':prueba,'query':query, 'enc':enc, 'pro':pro,'suma':suma})



@login_required(login_url='/login/')
@permission_required('che.change_cheque', login_url='bases:sin_privilegios')
def search(request):
    query = request.GET.get('q' , '')
    if query:
        qset = (
            # Q(cantidad=query)|
            Q(fecha_pagar=query)
            )
        cheques = Cheque.objects.filter(qset).order_by('-fc')
    else:
        cheques =[]

    return render(request , "che/busqueda_all_che.html" , { 'query' :query , 'cheques': cheques,
        })


@login_required(login_url='/login/')
@permission_required('che.change_cheque', login_url='bases:sin_privilegios')
def Vista_pagar(request):
    cheque = Cheque.objects.all()
    template_name = "che/cheque_pagar_pdf.html"

    context = {
        'cheque':  Cheque.objects.all()
    }

    return render(request, template_name, context)


@login_required(login_url='/login/')
@permission_required('che.change_cheque', login_url='bases:sin_privilegios')
def imprimir_che_pagar(request,f6):
    template_name = "che/cheque_print_pagar.html"
    enc=parse_date(f6)
    suma = 0
    if enc:
        qset = (

            Q(fecha_pagar=enc)
            )
        enc = Cheque.objects.filter(qset).order_by('-fc')
        suma = list(Cheque.objects.filter(qset).aggregate(Sum('cantidad')).values())[0]
    else:
        enc =[]
        suma=[]


    return render(request, template_name, {'f6': f6, 'enc': enc, 'suma':suma})



def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path


def reporte_che_entregados(request):
    template_path = 'che/che_pendientesPdf.html'
    today = timezone.now()

    cheque = Cheque.objects.filter(estado_che=False).order_by('-fc')
    context = {
        'cheque': cheque,
        'today': today,
        'reque': request
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="cheques_pendientes.pdf"'
    template= get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    if pisa_status.err:
        return HttpResponse('error <pre>' + html + '</pre>')
    return response


class ChequeEntregadoView(SuccessMessageMixin,SinPrivilegios, generic.ListView):
    permission_required = "che.view_cheque"
    model = Fisico_Entregado
    template_name = "che/cheque_entregado_list.html"


    def get_queryset(self):
        return self.model.objects.all().order_by('-fecha_creado')[:100]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ChequeEntregadoNew(SuccessMessageMixin,SinPrivilegios, generic.CreateView):
    permission_required = "che.add_cheque"
    model=Fisico_Entregado
    template_name="che/cheque_entregado_form.html"
    form_class = CheEntregadoForm
    success_url=reverse_lazy("che:che_entregado_list")

    def post(self, request, *args, **kwargs):
        form = CheEntregadoForm(request.POST, request.FILES)
        if form.is_valid():
            self.object = form.save(commit=False)
            form.instance.uc = self.request.user
            id_che = self.object.cheque.pk
            cheque_update = Cheque.objects.get(pk=id_che)
            cheque_update.estado_che = True
            form.save()
            cheque_update.save()
            return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, {'form': form})

class ChequeRechazadoView(SuccessMessageMixin,SinPrivilegios, generic.ListView):
    permission_required = "che.view_cheque"
    model = Cheque_rechazado
    template_name = "che/cheque_rechazado_list.html"


    def get_queryset(self):
        return self.model.objects.all().order_by('-fc')[:100]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ChequeRechazadoNew(SuccessMessageMixin,SinPrivilegios, generic.CreateView):
    permission_required = "che.add_cheque"
    model= Cheque_rechazado
    template_name="che/cheque_rechazado_form.html"
    form_class = CheRechazadoForm
    success_url=reverse_lazy("che:cheque_rechazado_list")

    def post(self, request, *args, **kwargs):
        form = CheRechazadoForm(request.POST)

        if form.is_valid():
            self.object = form.save(commit=False)
            form.instance.uc = self.request.user
            id_che = self.object.cheque_re.pk
            print(id_che)

            cheque_update = Cheque.objects.get(pk=id_che)
            cheque_update.status = 'E'
            cheque_update.save()

            id_fac = self.object.id_facturas.pk
            factura_update = Factura.objects.get(pk=id_fac)
            factura_update.total_fac1 = factura_update.total_fac1 + cheque_update.cantidad
            factura_update.save()

            form.save()
            return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, {'form': form})



class Abono_Fac(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    permission_required = "che.add_cheque"
    model = Abono_Factura
    template_name = "che/abono_factura_form.html"
    form_class = AbonoForm
    success_url=reverse_lazy("che:abono_factura_list")

    def post(self, request, *args, **kwargs):
        form = AbonoForm(request.POST)
        if form.is_valid():
            self.object = form.save(commit=False)
            form.instance.uc = self.request.user
            id_che = self.object.id_cheque.pk
            id_cheque = Cheque.objects.get(pk=id_che)
            id_facturas = self.object.id_factura.pk
            fac_update = Factura.objects.get(pk=id_facturas)
            fac_update.total_fac1 = fac_update.total_fac1 - id_cheque.cantidad
            form.save()
            fac_update.save()
            return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, {'form': form})



def cheques_rechazados(request, id , **kwargs):
    cheque = Cheque.objects.get(pk=id)
    cheque.status = 'E'
    cheque.save()
    #Agregar al historial
    return HttpResponseRedirect(reverse('che:search_che'))


class ChequeGeneratePendintesPDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('che/cheque_print_rechazados.html')
        cheque = Cheque.objects.filter(estado_che=False).order_by('-fc')
        params = {
            "cheque": cheque,


        }
        html = template.render(params)
        pdf = Render.render('', params)
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

class PDFPedidosHoy(PDFTemplateResponseMixin , TemplateView):
    redirect_field_name = 'redirect_to'
    template_name = 'che/report_cheques_del_dia.html'

    def get_context_data(self , *args , **kwargs):
        cheque = Cheque.objects.filter(estado_che=False, status=None).order_by('-fc')
        return {"cheque" : cheque}

@login_required(login_url='/login/')
@permission_required('che.change_cheque', login_url='bases:sin_privilegios')
def deposito_filter(request):
    query1 = request.GET.get('q', '')
    query2 = request.GET.get('p', 'p')
    if query1:
        if query2:
            inicio = datetime.strptime(query1, '%Y-%m-%d')
            final = datetime.strptime(query2, '%Y-%m-%d')
            deposito = Deposito.objects.filter(fecha_creado__range =[inicio , final]).order_by('-fecha_creado')
        else :
            deposito = []
            inicio = []
    else :
        final = []
        deposito = []

    return render(request , 'che/deposito_filter.html' , {'query1': query1 , 'query2' : query2 ,'deposito': deposito})

@login_required(login_url='/login/')
def search_factura(request):
    query = request.GET.get('q' , '')
    if query:
        qset = (
            Q(no_fac__icontains=query)
            # Q(username__nombres__icontains=query)|
            # Q(username__apellidos__icontains=query)
            )
        facturas = Factura.objects.filter(qset).order_by('-fc')
    else:
        facturas =[]

    return render(request , "che/busqueda_facturas.html" , { 'query' :query , 'facturas': facturas,
        })


class FacturaDetail(SuccessMessageMixin,SinPrivilegios, generic.DetailView):
    permission_required = "che.view_cheque"
    model = Factura
    template_name = 'che/factura_detalle.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['abonos_facturas'] = self.get_object().abonos_facturas

        context['form'] = AbonoForm({
            'factura_id' : self.get_object().id
        })
        return context

@login_required(login_url='/login/')
def search_cheque_numero(request):
    query = request.GET.get('q' , '')
    if query:
        qset = (
            Q(no_cheque__icontains=query)
            # Q(username__nombres__icontains=query)|
            # Q(username__apellidos__icontains=query)
            )
        cheque = Cheque.objects.filter(qset).order_by('-fc')
    else:
        cheque =[]

    return render(request , "che/busqueda_cheque_nuemero.html" , { 'query' :query , 'cheque': cheque,
        })
