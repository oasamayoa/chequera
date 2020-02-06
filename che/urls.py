from django.urls import path
from django_filters.views import FilterView
from django.contrib.auth import views as auth_views
from .views import ChequeView, Cheque_inactivar,  ChequeNew, ChequeEdit, ChequeGeneratePDF,  filter,\
        ChequeDetailView, BancoFilterView,ProveedorFilterView, imprimir_cheque_list, imprimir_cheque_img
from .models import Cheque




urlpatterns = [

        path('cheque/',ChequeView.as_view(), name='cheque_list'),
        path('cheque/new', ChequeNew.as_view(), name='cheque_new'),
        path('cheque/edit/<int:pk>',ChequeEdit.as_view(), name='cheque_edit'),
        path('cheque/estado/<int:id>', Cheque_inactivar, name='cheque_inactivar'),

        path('cheques/listado',ChequeGeneratePDF.as_view(), name='cheque_print_all'),
        path('cheque/imprimir-todas/<str:f1>/<str:f2>' , imprimir_cheque_list, name="cheque_print_all"),
        path('cheque/imprimir-imagen/<str:f1>/<str:f2>' , imprimir_cheque_img, name="cheque_print_img"),

        path('reporte/fecha/',filter, name = 'search_che'),
        path('reporte/banco/',BancoFilterView, name = 'search_banco'),
        path('reporte/proveedor/',ProveedorFilterView, name = 'search_proveedor'),


        path('detalle/cheque/<int:id>' , ChequeDetailView.as_view() , name='detail_cheque'),




]
