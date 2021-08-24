from django.db.models import Q, Count, Sum
from easy_pdf.views import PDFTemplateView, PDFTemplateResponseMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction


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

from .models import (
    Cheque,
    Deposito,
    Fisico_Entregado,
    Cheque_rechazado,
    Factura,
    Abono_Factura,
    Recibo,
)
from registro.models import Banco, Cuenta, Provedor
from che.forms import (
    ChequeForm,
    DepositoForm,
    CheEntregadoForm,
    CheRechazadoForm,
    FacturaForm,
    AbonoForm,
    ChequeEditform,
    AbonoEquivocadoForm,
    AbonoEditForm,
    DepositoEditForm,
    FacturaFormEdit,
    ReciboForm,
)
from bases.views import SinPrivilegios

from django.utils import timezone
from django.template.loader import get_template
from .utils import render_to_pdf, Render  # created in step 4
from django.views.generic import (
    TemplateView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    View,
)
import django_filters
from django.utils.dateparse import parse_date
from datetime import date, timedelta, datetime
import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


from .filter import ChequeFilter


class ChequeView(SuccessMessageMixin, SinPrivilegios, generic.ListView):
    permission_required = "che.view_cheque"
    model = Cheque
    template_name = "che/cheque_list.html"
    # paginate_by = 10 esta opcion sirve para cuantos elementos queres mostrar por pagina

    def get_queryset(self):
        return (
            self.model.objects.all()
            .select_related("cuenta", "proveedor", "id_fac")
            .order_by("-id")[0:100]
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DepositoView(SuccessMessageMixin, SinPrivilegios, generic.ListView):
    permission_required = "che.view_deposito"
    model = Deposito
    template_name = "che/deposito_list.html"

    def get_queryset(self):
        return self.model.objects.all().select_related("cheque").order_by("-id")[:100]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FacturaView(SuccessMessageMixin, SinPrivilegios, generic.ListView):
    permission_required = "che.view_factura"
    model = Factura
    template_name = "che/factura_list.html"

    def get_queryset(self):
        return (
            self.model.objects.all().select_related("proveedor").order_by("-id")[:800]
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class Abono_FacturaView(SuccessMessageMixin, SinPrivilegios, generic.ListView):
    permission_required = "che.view_factura"
    model = Abono_Factura
    template_name = "che/abono_factura_list.html"

    def get_queryset(self):
        try:
            if self.model.objects.latest("fc"):
                return self.model.objects.latest("fc")
        except self.model.DoesNotExist:
            abono = None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class Abono_EquivocadoView(SuccessMessageMixin, SinPrivilegios, generic.ListView):
    permission_required = "che.view_factura"
    model = Abono_Factura
    template_name = "che/abono_factura_equi_list.html"

    def get_queryset(self):
        try:
            if self.model.objects.latest("fc"):
                return self.model.objects.latest("fc")
        except self.model.DoesNotExist:
            abono = None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(context)
        return context


class ChequeNew(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    permission_required = "che.add_cheque"
    model = Cheque
    template_name = "che/cheque_form.html"
    context_object_name = "obj"
    form_class = ChequeForm
    success_url = reverse_lazy("che:cheque_list")

    def post(self, request, *args, **kwargs):
        form = ChequeForm(request.POST, request.FILES)
        if form.is_valid():
            self.object = form.save(commit=False)
            form.instance.uc = self.request.user
            che_form = form.save()
            if form:
                abono = Abono_Factura()
                id_facturas = self.object.id_fac.pk
                fac_update = Factura.objects.get(pk=id_facturas)
                abono.id = che_form.id
                abono.id_factura_id = fac_update.id
                abono.id_cheque_id = che_form.id
                abono.uc_id = self.request.user.pk
                fac_update.total_fac1 = float(fac_update.total_fac1) - float(
                    che_form.cantidad
                )
                fac_update.save()
                abono.save()
            return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, {"form": form})

    # def form_valid(self, form):
    #     form.instance.uc = self.request.user
    #     return super().form_valid(form)


class DepositoNew(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    permission_required = "che.add_deposito"
    model = Deposito
    template_name = "che/depo_form.html"
    context_object_name = "obj"
    form_class = DepositoForm
    success_url = reverse_lazy("che:deposito_list")

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
        return render(request, self.template_name, {"form": form})


class FacturaNew(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    permission_required = "che.add_cheque"
    model = Factura
    template_name = "che/factura_form.html"
    context_object_name = "obj"
    form_class = FacturaForm
    success_url = reverse_lazy("che:factura_list")

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


class ChequeEdit(SuccessMessageMixin, SinPrivilegios, generic.UpdateView):
    permission_required = "che.change_cheque"
    model = Cheque
    template_name = "che/cheque_form_edit.html"
    context_object_name = "obj"
    form_class = ChequeEditform
    success_url = reverse_lazy("che:cheque_list")

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class DepositoEdit(SuccessMessageMixin, SinPrivilegios, generic.UpdateView):
    permission_required = "che.change_deposito"
    model = Deposito
    template_name = "che/depo_form.html"
    context_object_name = "obj"
    form_class = DepositoEditForm
    success_url = reverse_lazy("che:deposito_list")

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class FacturaEdit(SuccessMessageMixin, SinPrivilegios, generic.UpdateView):
    permission_required = "che.delete_factura"
    model = Factura
    template_name = "che/factura_form.html"
    context_object_name = "obj"
    form_class = FacturaFormEdit
    success_url = reverse_lazy("che:factura_list")

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


@login_required(login_url="/login/")
@permission_required("che.change_cheque", login_url="bases:sin_privilegios")
def Cheque_inactivar(request, id):
    cheque = Cheque.objects.filter(pk=id).first()

    if request.method == "POST":
        if cheque:
            cheque.estado = not cheque.estado
            cheque.save()
            return HttpResponse("ok")
        return HttpResponse("FAIL")

    return HttpResponse("FAIL")


class ChequeDetailView(SuccessMessageMixin, SinPrivilegios, generic.DetailView):
    permission_required = "che.change_cheque"
    redirect_field_name = "redirect_to"
    template_name = "che/detail_cheque.html"
    slug_field = "id"
    slug_url_kwarg = "id"
    queryset = Cheque.objects.all()
    context_object_name = "cheque"


class DepositoDetailView(SuccessMessageMixin, SinPrivilegios, generic.DetailView):
    permission_required = "che.change_deposito"
    redirect_field_name = "redirect_to"
    template_name = "che/detail_deposito.html"
    slug_field = "id"
    slug_url_kwarg = "id"
    queryset = Deposito.objects.all()
    context_object_name = "deposito"


def is_valid_queryparam(param):
    return param != "" and param is not None


def Bancofilter(request):
    qs = Cheque.objects.all()
    proveedor = Provedor.objects.all()
    institucion = Cuenta.objects.all()
    bancario = Banco.objects.all()
    no_cheque_query = request.GET.get("no_cheque_query")
    cantidad_query = request.GET.get("cantidad_query")
    fecha_pagar_query = request.GET.get("fecha_pagar_query")
    no_fac_query = request.GET.get("no_fac_query")
    date_min = request.GET.get("date_min")
    date_max = request.GET.get("date_max")
    imagen_query = request.GET.get("imagen_query")
    cuenta_query = request.GET.get("cuenta_query")
    category = request.GET.get("category")
    categoria = request.GET.get("categoria")
    banco_query = request.GET.get("banco_query")

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

    if is_valid_queryparam(category) and category != "Choose...":
        qs = qs.filter(proveedor__nombre=category)

    if is_valid_queryparam(categoria) and categoria != "Choose...":
        qs = qs.filter(cuenta__nombre=categoria)

    if is_valid_queryparam(imagen_query):
        qs = qs.filter(imagen__icontains=imagen_query)

    if is_valid_queryparam(cuenta_query):
        qs = qs.filter(cuenta__icontains=cuenta_query)

    return qs


@login_required(login_url="/login/")
@permission_required("che.change_cheque", login_url="bases:sin_privilegios")
def BancoFilterView(request):
    # qs = Bancofilter(request)
    value = request.GET.get("date_min", "")
    if value:
        qs = Bancofilter(request)
    else:
        qs = {}
    context = {
        "queryset": qs,
        "proveedor": Provedor.objects.all(),
        "institucion": Cuenta.objects.all(),
    }
    return render(request, "che/search_banco.html", context)


@login_required(login_url="/login/")
@permission_required("che.change_cheque", login_url="bases:sin_privilegios")
def ProveedorFilterView(request):
    # qs = Bancofilter(request)
    value = request.GET.get("date_min", "")
    if value:
        qs = Bancofilter(request)
    else:
        qs = {}
    context = {
        "queryset": qs,
        "proveedor": Provedor.objects.all(),
        "institucion": Cuenta.objects.all(),
    }
    return render(request, "che/search_proveedor.html", context)


@login_required(login_url="/login/")
@permission_required("che.change_cheque", login_url="bases:sin_privilegios")
def filter(request):
    query1 = request.GET.get("q", "")
    query2 = request.GET.get("p", "p")
    if query1:
        if query2:
            inicio = datetime.strptime(query1, "%Y-%m-%d")
            final = datetime.strptime(query2, "%Y-%m-%d")
            cheque = Cheque.objects.filter(
                fecha_creado__range=[inicio, final]
            ).order_by("-fecha_creado")
        else:
            cheque = []
            inicio = []
    else:
        final = []
        cheque = []

    return render(
        request,
        "che/che_form.html",
        {"query1": query1, "query2": query2, "cheque": cheque},
    )


class ChequeGeneratePDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template("che/cheque_print_all.html")
        cheque = Cheque.objects.all()
        params = {
            "cheque": cheque,
        }
        html = template.render(params)
        pdf = Render.render("", params)
        if pdf:
            response = HttpResponse(pdf, content_type="application/pdf")
            filename = "Invoice_%s.pdf" % ("12341231")
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response["Content-Disposition"] = content
            return response
        return HttpResponse("Not found")


@login_required(login_url="/login/")
@permission_required("che.change_cheque", login_url="bases:sin_privilegios")
def imprimir_cheque_list(request, f1, f2):
    try:
        template = get_template("che/cheque_print_all.html")
        f1 = parse_date(f1)
        f2 = parse_date(f2)
        enc = Cheque.objects.filter(fecha_creado__range=[f1, f2]).order_by(
            "-fecha_creado"
        )
        suma = 0
        for cheque in enc:
            suma = suma + cheque.cantidad

        context = {"request": request, "f1": f1, "f2": f2, "enc": enc, "suma": suma}
        html = template.render(context)
        response = HttpResponse(content_type="application/pdf")
        # response['Content-Disposition'] = 'attachment; filename="report.pdf"' # esta parte es para que se descargue le pdf
        pisa_status = pisa.CreatePDF(html, dest=response)
        return response
    except:
        pass
    return HttpResponseRedirect(reverse_lazy("che:cheque_list"))


@login_required(login_url="/login/")
@permission_required("che.change_deposito", login_url="bases:sin_privilegios")
def imprimir_deposito_list(request, f1, f2):
    try:
        template = get_template("che/deposito_print_all.html")
        f1 = parse_date(f1)
        f2 = parse_date(f2)
        enc = Deposito.objects.filter(fecha_creado__range=[f1, f2]).order_by(
            "-fecha_creado"
        )
        suma = 0
        for deposito in enc:
            suma = suma + deposito.cantidad
        context = {"request": request, "f1": f1, "f2": f2, "enc": enc, "suma": suma}
        html = template.render(context)
        response = HttpResponse(content_type="application/pdf")
        # response['Content-Disposition'] = 'attachment; filename="report.pdf"' # esta parte es para que se descargue le pdf
        pisa_status = pisa.CreatePDF(html, dest=response)
        return response
    except:
        pass
    return HttpResponseRedirect(reverse_lazy("che:deposito_list"))


class imprimir_cheque_img(View):
    def link_callback(self, uri, rel):
        """
        Es la Función para poder convertir un archivo html a pdf
        """
        result = finders.find(uri)
        if result:
            if not isinstance(result, (list, tuple)):
                result = [result]
            result = list(os.path.realpath(path) for path in result)
            path = result[0]
        else:
            sUrl = settings.STATIC_URL
            sRoot = settings.STATIC_ROOT
            mUrl = settings.MEDIA_URL
            mRoot = settings.MEDIA_ROOT

            if uri.startswith(mUrl):
                path = os.path.join(mRoot, uri.replace(mUrl, ""))
            elif uri.startswith(sUrl):
                path = os.path.join(sRoot, uri.replace(sUrl, ""))
            else:
                return uri

        if not os.path.isfile(path):
            raise Exception("media URI must start with %s or %s" % (sUrl, mUrl))
        return path

    def get(self, request, f1, f2, *args, **kwargs):
        try:
            template = get_template("che/cheque_print_img.html")
            f1 = parse_date(f1)
            f2 = parse_date(f2)
            enc = Cheque.objects.filter(fecha_creado__range=[f1, f2]).order_by(
                "-fecha_creado"
            )
            suma = 0
            for cheque in enc:
                suma = suma + cheque.cantidad

            context = {"request": request, "f1": f1, "f2": f2, "enc": enc, "suma": suma}
            html = template.render(context)
            response = HttpResponse(content_type="application/pdf")
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"' # esta parte es para que se descargue le pdf
            pisa_status = pisa.CreatePDF(
                html, dest=response, link_callback=self.link_callback
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy("che:cheque_list"))


# def imprimir_cheque_img(request, f1,f2):
#     try:
#         template = get_template('che/cheque_print_img.html')
#         f1=parse_date(f1)
#         f2=parse_date(f2)
#         enc = Cheque.objects.filter(fecha_creado__range = [f1 , f2]).order_by('-fecha_creado')
#         suma = 0
#         for cheque in enc:
#             suma = suma+cheque.cantidad
#
#         context = {
#             'request': request,
#             'f1':f1,
#             'f2':f2,
#             'enc':enc,
#             'suma':suma
#
#         }
#         html = template.render(context)
#         response = HttpResponse(content_type='application/pdf')
#         # response['Content-Disposition'] = 'attachment; filename="report.pdf"' # esta parte es para que se descargue le pdf
#         pisa_status = pisa.CreatePDF(
#             html, dest=response,
#             link_callback=self.link_callback)
#         return response
#     except:
#         pass
#     return HttpResponseRedirect(reverse_lazy('che:cheque_list'))


@login_required(login_url="/login/")
@permission_required("che.change_cheque", login_url="bases:sin_privilegios")
def Vista_Proveedor(request):
    categoria = Provedor.objects.all()
    results = Cheque.objects.all()
    template_name = "che/cheque_vista_pdf.html"

    context = {"categoria": Provedor.objects.all(), "results": Cheque.objects.all()}

    return render(request, template_name, context)


@login_required(login_url="/login/")
@permission_required("che.change_cheque", login_url="bases:sin_privilegios")
def imprimir_provedor(request, f5, f6, categoria):
    try:
        template = get_template("che/cheque_print_prove.html")
        f5 = parse_date(f5)
        f6 = parse_date(f6)
        enc = Cheque.objects.filter(
            fecha_creado__range=[f5, f6], proveedor=categoria
        ).order_by("-fecha_creado")
        suma = 0
        for cheque in enc:
            suma = suma + cheque.cantidad

        context = {
            "f5": f5,
            "f6": f6,
            "categoria": categoria,
            "enc": enc,
            "suma": suma,
        }
        html = template.render(context)
        response = HttpResponse(content_type="application/pdf")
        # response['Content-Disposition'] = 'attachment; filename="report.pdf"' # esta parte es para que se descargue le pdf
        pisa_status = pisa.CreatePDF(html, dest=response)
        return response
    except:
        pass
    return HttpResponseRedirect(reverse_lazy("che:factura_list"))


@login_required(login_url="/login/")
@permission_required("che.change_cheque", login_url="bases:sin_privilegios")
def Vista_Banco(request):
    categoria = Cuenta.objects.all()
    cheque = Cheque.objects.all()
    template_name = "che/cheque_vista_bancopdf.html"

    context = {"categoria": Cuenta.objects.all(), "cheque": Cheque.objects.all()}

    return render(request, template_name, context)


@login_required(login_url="/login/")
@permission_required("che.change_cheque", login_url="bases:sin_privilegios")
def imprimir_banco(request, f5, f6, categoria):
    template_name = "che/cheque_print_banco.html"
    f5 = parse_date(f5)
    f6 = parse_date(f6)
    prueba = []
    pro = []
    query = []
    enc = Cheque.objects.filter(
        fecha_creado__range=[f5, f6], cuenta__nombre=categoria
    ).order_by("-fecha_creado")

    # tot = Cheque.objects.filter(fecha_creado__range = [f5, f6], cuenta__nombre=categoria).aggregate(Sum('cantidad'))
    suma = 0
    for cheque in enc:
        suma = suma + cheque.cantidad
    return render(
        request,
        template_name,
        {
            "f5": f5,
            "f6": f6,
            "categoria": categoria,
            "prueba": prueba,
            "query": query,
            "enc": enc,
            "pro": pro,
            "suma": suma,
        },
    )


@login_required(login_url="/login/")
@permission_required("che.change_cheque", login_url="bases:sin_privilegios")
def search(request):
    query = request.GET.get("q", "")
    if query:
        qset = (
            # Q(cantidad=query)|
            Q(fecha_pagar=query)
        )
        cheques = Cheque.objects.filter(qset).order_by("-fc")
    else:
        cheques = []

    return render(
        request,
        "che/busqueda_all_che.html",
        {
            "query": query,
            "cheques": cheques,
        },
    )


@login_required(login_url="/login/")
@permission_required("che.change_cheque", login_url="bases:sin_privilegios")
def Vista_pagar(request):
    cheque = Cheque.objects.all()
    template_name = "che/cheque_pagar_pdf.html"

    context = {"cheque": Cheque.objects.all()}

    return render(request, template_name, context)


@login_required(login_url="/login/")
@permission_required("che.change_cheque", login_url="bases:sin_privilegios")
def imprimir_che_pagar(request, f6):
    try:
        template = get_template("che/cheque_print_pagar.html")
        enc = parse_date(f6)
        if enc:
            qset = Q(fecha_pagar=enc)
            enc = Cheque.objects.filter(qset).order_by("-fc")
            suma = list(
                Cheque.objects.filter(qset).aggregate(Sum("cantidad")).values()
            )[0]
        else:
            enc = []
            suma = []
        context = {"request": request, "enc": enc, "suma": suma}
        html = template.render(context)
        response = HttpResponse(content_type="application/pdf")
        # response['Content-Disposition'] = 'attachment; filename="report.pdf"' # esta parte es para que se descargue le pdf
        pisa_status = pisa.CreatePDF(html, dest=response)
        return response
    except:
        pass
    return HttpResponseRedirect(reverse_lazy("che:cheque_pagar"))


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL  # Typically /static/
    sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL  # Typically /static/media/
    mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception("media URI must start with %s or %s" % (sUrl, mUrl))
    return path


def reporte_che_entregados(request):
    template_path = "che/che_pendientesPdf.html"
    today = timezone.now()

    cheque = Cheque.objects.filter(estado_che=False).order_by("-fc")
    context = {"cheque": cheque, "today": today, "reque": request}
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="cheques_pendientes.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisa_status.err:
        return HttpResponse("error <pre>" + html + "</pre>")
    return response


class ChequeEntregadoView(SuccessMessageMixin, SinPrivilegios, generic.ListView):
    permission_required = "che.view_cheque"
    model = Fisico_Entregado
    template_name = "che/cheque_entregado_list.html"

    def get_queryset(self):
        return self.model.objects.all().order_by("-fecha_creado")[:100]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ChequeEntregadoNew(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    permission_required = "che.add_cheque"
    model = Fisico_Entregado
    template_name = "che/cheque_entregado_form.html"
    form_class = CheEntregadoForm
    success_url = reverse_lazy("che:che_entregado_list")

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
        return render(request, self.template_name, {"form": form})


class ChequeRechazadoView(SuccessMessageMixin, SinPrivilegios, generic.ListView):
    permission_required = "che.view_cheque"
    model = Cheque_rechazado
    template_name = "che/cheque_rechazado_list.html"

    def get_queryset(self):
        return self.model.objects.all().order_by("-fc")[:100]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ChequeRechazadoNew(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    permission_required = "che.add_cheque"
    model = Cheque_rechazado
    template_name = "che/cheque_rechazado_form.html"
    form_class = CheRechazadoForm
    success_url = reverse_lazy("che:cheque_rechazado_list")

    def post(self, request, *args, **kwargs):
        form = CheRechazadoForm(request.POST)

        if form.is_valid():
            self.object = form.save(commit=False)
            form.instance.uc = self.request.user
            id_che = self.object.cheque_re.pk
            id_che_nu = self.object.cheque_nu.pk

            cheque_nuevo = Cheque.objects.get(pk=id_che_nu)
            cheque_update = Cheque.objects.get(pk=id_che)
            cheque_update.status = "E"
            cheque_update.save()

            id_fac = self.object.id_facturas.pk
            factura_update = Factura.objects.get(pk=id_fac)
            resultado = (
                float(factura_update.total_fac1)
                + float(cheque_update.cantidad)
                - float(cheque_nuevo.cantidad)
            )
            abono = Abono_Factura.objects.update_or_create(
                pk=id_che_nu,
                defaults={
                    "id_cheque": cheque_nuevo,
                    "cheque_equivocado": cheque_update,
                    "estado_abono": False,
                    "id_factura": factura_update,
                },
            )
            factura_update.total_fac1 = resultado
            factura_update.save()
            form.save()
            return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, {"form": form})


class Abono_Fac(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    permission_required = "che.add_cheque"
    model = Abono_Factura
    template_name = "che/abono_factura_form.html"
    form_class = AbonoForm
    success_url = reverse_lazy("che:abono_factura_list")

    def post(self, request, *args, **kwargs):
        form = AbonoForm(request.POST)
        if form.is_valid():
            self.object = form.save(commit=False)
            form.instance.uc = self.request.user
            id_che = self.object.id_cheque.pk
            id_cheque = Cheque.objects.get(pk=id_che)
            id_facturas = self.object.id_factura.pk
            fac_update = Factura.objects.get(pk=id_facturas)
            fac_update.total_fac1 = float(fac_update.total_fac1) - float(
                id_cheque.cantidad
            )
            form.save()
            fac_update.save()
            return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, {"form": form})


class Abono_Fac_edit(SuccessMessageMixin, SinPrivilegios, generic.UpdateView):
    permission_required = "che.change_abono_factura"
    model = Abono_Factura
    template_name = "che/abono_factura_form_edit.html"
    context_object_name = "obj"
    form_class = AbonoEditForm
    success_url = reverse_lazy("che:abono_factura_list")

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        id_facturas = self.object.id_factura.pk
        id_che = self.object.id_cheque.pk
        id_cheque = Cheque.objects.get(pk=id_che)
        fac_update = Factura.objects.get(pk=id_facturas)
        fac_update.total_fac1 = float(fac_update.total_fac1) - float(id_cheque.cantidad)
        fac_update.save()
        return super().form_valid(form)


class Abono_Fac_equi_edit(SuccessMessageMixin, SinPrivilegios, generic.UpdateView):
    permission_required = "che.change_abono_factura"
    model = Abono_Factura
    template_name = "che/abono_factura_equi_form.html"
    context_object_name = "obj"
    form_class = AbonoEquivocadoForm
    success_url = reverse_lazy("che:abono_factura_list")

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class Abonos_equivocados(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    permission_required = "che.add_cheque"
    model = Abono_Factura
    template_name = "che/abono_factura_equi_form.html"
    form_class = AbonoEquivocadoForm
    success_url = reverse_lazy("che:abono_factura_equi_list")

    def post(self, request, *args, **kwargs):
        form = AbonoEquivocadoForm(request.POST)
        if form.is_valid():
            self.object = form.save(commit=False)
            form.instance.uc = self.request.user
            id_che = self.object.id_cheque.pk
            id_re = self.object.cheque_equivocado.pk
            id_recha = Cheque.objects.get(pk=id_re)
            id_cheque = Cheque.objects.get(pk=id_che)
            id_facturas = self.object.id_factura.pk
            fac_update = Factura.objects.get(pk=id_facturas)
            id_recha.estado = id_recha.estado = False
            id_recha.save()
            form.save()

            return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, {"form": form})


def cheques_rechazados(request, id, **kwargs):
    cheque = Cheque.objects.get(pk=id)
    cheque.status = "E"
    cheque.save()
    # Agregar al historial
    return HttpResponseRedirect(reverse("che:search_che"))


class ChequeGeneratePendintesPDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template("che/cheque_print_rechazados.html")
        cheque = Cheque.objects.filter(estado_che=False).order_by("-fc")
        params = {
            "cheque": cheque,
        }
        html = template.render(params)
        pdf = Render.render("", params)
        if pdf:
            response = HttpResponse(pdf, content_type="application/pdf")
            filename = "Invoice_%s.pdf" % ("12341231")
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response["Content-Disposition"] = content
            return response
        return HttpResponse("Not found")


class PDFPedidosHoy(PDFTemplateResponseMixin, TemplateView):
    redirect_field_name = "redirect_to"
    template_name = "che/report_cheques_del_dia.html"

    def get_context_data(self, *args, **kwargs):
        cheque = Cheque.objects.filter(estado_che=False, status=None).order_by("-fc")
        return {"cheque": cheque}


@login_required(login_url="/login/")
@permission_required("che.change_cheque", login_url="bases:sin_privilegios")
def deposito_filter(request):
    query1 = request.GET.get("q", "")
    query2 = request.GET.get("p", "p")
    if query1:
        if query2:
            inicio = datetime.strptime(query1, "%Y-%m-%d")
            final = datetime.strptime(query2, "%Y-%m-%d")
            deposito = Deposito.objects.filter(
                fecha_creado__range=[inicio, final]
            ).order_by("-fecha_creado")
        else:
            deposito = []
            inicio = []
    else:
        final = []
        deposito = []

    return render(
        request,
        "che/deposito_filter.html",
        {"query1": query1, "query2": query2, "deposito": deposito},
    )


@login_required(login_url="/login/")
def search_factura(request):
    query = request.GET.get("q", "")
    if query:
        qset = (
            Q(no_fac__icontains=query)
            # Q(username__nombres__icontains=query)|
            # Q(username__apellidos__icontains=query)
        )
        facturas = Factura.objects.filter(qset).order_by("-fc")
    else:
        facturas = []

    return render(
        request,
        "che/busqueda_facturas.html",
        {
            "query": query,
            "facturas": facturas,
        },
    )


class FacturaDetail(SuccessMessageMixin, SinPrivilegios, generic.DetailView):
    permission_required = "che.view_cheque"
    model = Factura
    template_name = "che/factura_detalle.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["abonos_facturas"] = self.get_object().abonos_facturas

        context["form"] = AbonoForm({"factura_id": self.get_object().id})

        return context


@login_required(login_url="/login/")
def search_cheque_numero(request):
    query = request.GET.get("q", "")
    if query:
        qset = (
            Q(no_cheque__icontains=query)
            # Q(username__nombres__icontains=query)|
            # Q(username__apellidos__icontains=query)
        )
        cheque = Cheque.objects.filter(qset).order_by("-fc")
    else:
        cheque = []

    return render(
        request,
        "che/busqueda_cheque_nuemero.html",
        {
            "query": query,
            "cheque": cheque,
        },
    )


class PDFFacturasNegativos(PDFTemplateResponseMixin, TemplateView):
    redirect_field_name = "redirect_to"
    template_name = "che/report_cheque_negativo.html"

    def get_context_data(self, *args, **kwargs):
        factura = Factura.objects.filter(total_fac1__lt=0).order_by("-fc")
        return {"factura": factura}


class PDFHistorial_Cheques(PDFTemplateResponseMixin, TemplateView):
    redirect_field_name = "redirect_to"
    template_name = "che/reporte_historial.html"
    model = Abono_Factura

    def get_context_data(self, *args, **kwargs):

        factura = Abono_Factura.objects.all()

        return {"factura": factura}


def factura_modal_proveedor(request):
    proveedor = Provedor.objects.all()
    fac = Factura.objects.all()
    template_name = "che/factura_modal_proveedor.html"

    context = {"proveedor": proveedor, "fac": fac}
    return render(request, template_name, context)


def factura_proveedor_pdf(request, f1, f2, proveedor):
    try:
        template = get_template("che/factura_proveedor_pdf.html")
        f1 = parse_date(f1)
        f2 = parse_date(f2)
        suma = 0
        enc = Factura.objects.filter(
            fc__range=[f1, f2], proveedor__nombre=proveedor
        ).order_by("-id")
        for m in Factura.objects.filter(
            total_fac1__gt=0, proveedor__nombre=proveedor
        ).order_by("-id"):
            suma = suma + m.total_fac1
        context = {"proveedor": proveedor, "f1": f1, "f2": f2, "enc": enc, "suma": suma}
        html = template.render(context)
        response = HttpResponse(content_type="application/pdf")
        # response['Content-Disposition'] = 'attachment; filename="report.pdf"' # esta parte es para que se descargue le pdf
        pisa_status = pisa.CreatePDF(html, dest=response)
        return response
    except:
        pass
    return HttpResponseRedirect(reverse_lazy("che:factura_list"))


class Recibo_create(generic.CreateView):
    template_name = "che/recibo_create.html"
    model = Recibo
    success_url = reverse_lazy("che:recibo_create")
    form_class = ReciboForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = request.user
        data = {}
        try:
            action = request.POST["action"]
            if action == "search_factura":
                data = []
                term = request.POST["term"]
                factura = Factura.objects.filter(total_fac1__gt=0)
                if len(term):
                    factura = factura.filter(no_fac__icontains=term)
                for i in factura[0:5]:
                    item = i.toJSON()
                    item["text"] = i.get_factura_name()
                    data.append(item)
            elif action == "add":
                recibo = request.method == "POST"
                form = ReciboForm(request.POST)
                if form.is_valid():
                    self.object = form.save(commit=False)
                    recibo_s = form.save()
                    if form:
                        with transaction.atomic():
                            id_facturas = self.object.factura.pk
                            fac_update = Factura.objects.get(pk=id_facturas)
                            fac_update.total_fac1 -= recibo_s.monto
                            fac_update.save()
                            recibo_s.save()
                            abono = Abono_Factura()
                            user = request.user.pk
                            abono.uc_id = user
                            abono.id_factura_id = fac_update.id
                            abono.estado_abono = True
                            abono.recibo_id = recibo_s.id
                            abono.save()

                    return HttpResponseRedirect(self.success_url)
                return render(request, self.template_name, {"form": form})
            else:
                data["error"] = "No ha ingresado a ninguna opción"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "add"
        context["list"] = self.success_url
        return context
