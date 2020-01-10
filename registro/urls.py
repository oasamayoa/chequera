from django.urls import path
from django_filters.views import FilterView
from django.contrib.auth import views as auth_views
from .views import BancoView, BancoNew, BancoEdit,CuentaView, CuentaNew, CuentaEdit, \
    cuenta_inactivar, banco_inactivar, ProveedorView, ProveedorNew, ProveedorEdit, proveedor_inactivar
from .models import Cuenta

urlpatterns = [
    path('bancos/',BancoView.as_view(), name='banco_list'),
    path('bancos/new',BancoNew.as_view(), name='banco_new'),
    path('bancos/edit/<int:pk>',BancoEdit.as_view(), name='banco_edit'),
    path('bancos/delete/<int:id>',banco_inactivar, name='banco_del'),

    path('cuenta/',CuentaView.as_view(), name='cuenta_list'),
    path('cuenta/new',CuentaNew.as_view(), name='cuenta_new'),
    path('cuenta/edit/<int:pk>',CuentaEdit.as_view(), name='cuenta_edit'),
    path('cuenta/delete/<int:id>',cuenta_inactivar, name='cuenta_del'),

    path('proveedor/',ProveedorView.as_view(), name='provedor_list'),
    path('proveedor/new',ProveedorNew.as_view(), name='provedor_new'),
    path('proveedor/edit/<int:pk>',ProveedorEdit.as_view(), name='provedor_edit'),
    path('proveedor/delete/<int:id>',proveedor_inactivar, name='provedor_del'),

    path('eje/', FilterView.as_view(model=Cuenta)),

]
