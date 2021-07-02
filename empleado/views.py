from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.views import generic
from django.urls import reverse_lazy, reverse
from django.views.generic import View, TemplateView, CreateView, UpdateView, DetailView
from empleado.models import Empleado, Farmacia
from empleado.forms import FarmaciaForm
from bases.views import SinPrivilegios

class EmpleadoView(SuccessMessageMixin,SinPrivilegios, generic.ListView):
    permission_required = "empleado.view_empleado"
    model = Empleado
    template_name = "empleado/empleado_list.html"

    def get_queryset(self):
        return self.model.objects.all().order_by('-fc')[:100]

    def context_object_data(self, *args, **kwargs):
        context = super().context_object_data(**kwargs)
        return context

class FarmaciaView(SuccessMessageMixin,SinPrivilegios, generic.ListView):
    permission_required = "empleado.view_farmacia"
    model = Farmacia
    template_name = "empleado/farmacia_list.html"

    def get_queryset(self):
        return self.model.objects.all().order_by('-fc')[:100]

    def context_object_data(self, *args, **kwargs):
        context = super().context_object_data(**kwargs)

        return context

class FarmaciaNew(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    permission_required = "empleado.add_cheque"
    model=Farmacia
    template_name="empleado/snippets/farmacia_new.html"
    context_object_name = "obj"
    form_class = FarmaciaForm
    success_url=reverse_lazy("empleado:farmacia_list")

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)
