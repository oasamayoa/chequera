from django.urls import path
from django_filters.views import FilterView
from django.contrib.auth import views as auth_views
from .views import ChequeView, ChequeNew, ChequeEdit, ChequeGeneratePDF,  filter, ChequeDetailView, BancoFilterView
from .models import Cheque




urlpatterns = [

        path('cheque/',ChequeView.as_view(), name='cheque_list'),
        path('cheque/new',ChequeNew.as_view(), name='cheque_new'),
        path('cheque/edit/<int:pk>',ChequeEdit.as_view(), name='cheque_edit'),

        path('cheques/listado',ChequeGeneratePDF.as_view(), name='cheque_print_all'),

        path('reporte/fecha/',filter, name = 'search_che'),
        path('reporte/banco/',BancoFilterView, name = 'search_banco'),


        path('detalle/cheque/<int:id>' , ChequeDetailView.as_view() , name='detail_cheque'),


]
