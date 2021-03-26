from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.views import generic
from django.views.generic import View, TemplateView, CreateView, UpdateView, DetailView
from empleado.models import Empleado
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
