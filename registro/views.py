from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from django.urls import reverse_lazy

from .models import Banco, Cuenta, Provedor
from .forms import BancoForm, CuentaForm, ProveedorForm
from bases.views import SinPrivilegios


class MixinFormInvalid:
    def form_invalid(self,form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response


class BancoView(SinPrivilegios, generic.ListView):
    permission_required = "registro.view_banco"
    model = Banco
    template_name = "registro/banco_list.html"
    context_object_name = "obj"


class BancoNew(SuccessMessageMixin,MixinFormInvalid,SinPrivilegios,generic.CreateView):
    permission_required = "registro.add_banco"
    model=Banco
    template_name="registro/banco_form.html"
    context_object_name = "obj"
    form_class = BancoForm
    success_url=reverse_lazy("registro:banco_list")
    success_message = "Banco Creado Satisfactoriamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class BancoEdit(SuccessMessageMixin,MixinFormInvalid,SinPrivilegios, generic.UpdateView):
    permission_required = "registro.edit_banco"
    model=Banco
    template_name="registro/banco_form.html"
    context_object_name = "obj"
    form_class = BancoForm
    success_url=reverse_lazy("registro:banco_list")
    success_message = "Banco editado Satisfactoriamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

@login_required(login_url='/login/')
@permission_required('registro.change_marca', login_url='bases:sin_privilegios')
def banco_inactivar(request, id):
    template_name='registro/inactivar_banco.html'
    contexto={}
    pro = Banco.objects.filter(pk=id).first()

    if not pro:
        return HttpResponse('Banco no existe ' + str(id))

    if request.method=='GET':
        contexto={'obj':pro}

    if request.method=='POST':
        pro.estado=False
        pro.save()
        contexto={'obj':'OK'}
        return HttpResponse('Banco Inactivado')

    return render(request,template_name,contexto)

def proveedor_inactivar(request,id):
    template_name='registro/inactivar_pro.html'
    contexto={}
    pro = Provedor.objects.filter(pk=id).first()

    if not pro:
        return HttpResponse('Proveedor no existe ' + str(id))

    if request.method=='GET':
        contexto={'obj':pro}

    if request.method=='POST':
        pro.estado=False
        pro.save()
        contexto={'obj':'OK'}
        return HttpResponse('Proveedor Inactivado')

    return render(request,template_name,contexto)

# este es para cuando deso borrar un dato por completo de la base de datos
# class CategoriaDel(LoginRequiredMixin, generic.DeleteView):
#
#     model=Banco
#     template_name="registro/catalogos_del.html"
#     context_object_name = "obj"
#     success_url=reverse_lazy("registro:banco_list")
#     login_url="bases:login"
#
#     def form_valid(self, form):
#         form.instance.um = self.request.user.id
#         return super().form_valid(form)

class CuentaView(SinPrivilegios, generic.ListView):
    permission_required = "registro.view_cuenta"
    model = Cuenta
    template_name = "categoria/cuenta_list.html"
    context_object_name = "obj"


class CuentaNew(SuccessMessageMixin,SinPrivilegios, generic.CreateView):
    permission_required = "registro.add_cuenta"
    model=Cuenta
    template_name="registro/cuenta_form.html"
    context_object_name = "obj"
    form_class = CuentaForm
    success_url=reverse_lazy("registro:cuenta_list")
    success_message = "Cuenta creada Satisfactoriamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class CuentaEdit(SuccessMessageMixin,SinPrivilegios, generic.UpdateView):
    permission_required = "registro.edit_cuenta"
    model=Cuenta
    template_name="registro/cuenta_form.html"
    context_object_name = "obj"
    form_class = CuentaForm
    success_url=reverse_lazy("registro:cuenta_list")
    success_message = "Cuenta editada Satisfactoriamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

# class CuentaCategoriaDel(LoginRequiredMixin, generic.DeleteView):
#
#     model=Cuenta
#     template_name="registro/catalogos_del.html"
#     context_object_name = "obj"
#     success_url=reverse_lazy("registro:cuenta_list")
#     login_url="bases:login"
#
#     def form_valid(self, form):
#         form.instance.um = self.request.user.id
#         return super().form_valid(form)

@login_required(login_url='/login/')
@permission_required('registro.change_marca', login_url='bases:sin_privilegios')
def cuenta_inactivar(request, id):
    template_name='registro/inactivar_cuenta.html'
    contexto={}
    pro = Cuenta.objects.filter(pk=id).first()

    if not pro:
        return HttpResponse('Cuenta no existe ' + str(id))

    if request.method=='GET':
        contexto={'obj':pro}

    if request.method=='POST':
        pro.estado=False
        pro.save()
        contexto={'obj':'OK'}
        return HttpResponse('Cuenta Inactivada')

    return render(request,template_name,contexto)

class ProveedorView(SinPrivilegios, generic.ListView):
    permission_required = "registro.view_provedor"
    model = Provedor
    template_name = "categoria/provedor_list.html"
    context_object_name = "obj"

class ProveedorNew(SinPrivilegios,MixinFormInvalid, generic.CreateView):
    permission_required = "registro.add_provedor"
    model=Provedor
    template_name="registro/provedor_form.html"
    context_object_name = "obj"
    form_class = ProveedorForm
    success_url=reverse_lazy("registro:provedor_list")

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


class ProveedorEdit(SinPrivilegios,MixinFormInvalid, generic.UpdateView):
    permission_required = "registro.edit_provedor"
    model=Provedor
    template_name="registro/provedor_form.html"
    context_object_name = "obj"
    form_class = ProveedorForm
    success_url=reverse_lazy("registro:provedor_list")

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

@login_required(login_url='/login/')
@permission_required('inv.change_marca', login_url='bases:sin_privilegios')
def proveedor_inactivar(request,id):
    template_name='registro/inactivar_pro.html'
    contexto={}
    pro = Provedor.objects.filter(pk=id).first()

    if not pro:
        return HttpResponse('Proveedor no existe ' + str(id))

    if request.method=='GET':
        contexto={'obj':pro}

    if request.method=='POST':
        pro.estado=False
        pro.save()
        contexto={'obj':'OK'}
        return HttpResponse('Proveedor Inactivado')

    return render(request,template_name,contexto)
