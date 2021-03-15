from django.urls import path
from django_filters.views import FilterView
from django.contrib.auth import views as auth_views
from .views import ChequeView, Cheque_inactivar,  ChequeNew, ChequeEdit, ChequeGeneratePDF,  filter,\
        ChequeDetailView, BancoFilterView,ProveedorFilterView, imprimir_cheque_list, imprimir_cheque_img,\
        imprimir_provedor, Vista_Proveedor, Vista_Banco, imprimir_banco, DepositoView, DepositoNew, DepositoEdit,\
        imprimir_deposito_list, DepositoDetailView, search, Vista_pagar, imprimir_che_pagar, reporte_che_entregados,\
        ChequeEntregadoView, ChequeEntregadoNew, cheques_rechazados, ChequeRechazadoView, ChequeRechazadoNew,\
        ChequeGeneratePendintesPDF, PDFPedidosHoy, deposito_filter, FacturaView, FacturaNew, FacturaEdit, \
        Abono_FacturaView, Abono_Fac
from .models import Cheque




urlpatterns = [

        path('cheque/',ChequeView.as_view(), name='cheque_list'),
        path('cheque/new', ChequeNew.as_view(), name='cheque_new'),
        path('cheque/edit/<int:pk>',ChequeEdit.as_view(), name='cheque_edit'),
        path('cheque/estado/<int:id>', Cheque_inactivar, name='cheque_inactivar'),

        path('cheques/listado',ChequeGeneratePDF.as_view(), name='cheque_print_all_all'),
        path('cheque/imprimir-todas/<str:f1>/<str:f2>' , imprimir_cheque_list, name="cheque_print_all"),
        path('cheque/imprimir-imagen/<str:f1>/<str:f2>' , imprimir_cheque_img, name="cheque_print_img"),
        path('cheque/pdfproveedor/<str:f5>/<str:f6>/<str:categoria>', imprimir_provedor, name="proveedor_print_prove"),
        path('cheque/pdfbanco/<str:f5>/<str:f6>/<str:categoria>', imprimir_banco, name="cheque_print_banco"),
        path('cheque/pdfpragar/<str:f6>/', imprimir_che_pagar, name="cheque_print_pagar"),

        path('reporte/fecha/',filter, name = 'search_che'),
        path('reporte/banco/',BancoFilterView, name = 'search_banco'),
        path('reporte/proveedor/',ProveedorFilterView, name = 'search_proveedor'),


        path('detalle/cheque/<int:id>' , ChequeDetailView.as_view() , name='detail_cheque'),
        path('cheque/detalle' , Vista_Proveedor, name='cheque_detalle'),
        path('cheque/banco' , Vista_Banco, name='banco_detalle'),
        path('cheque/pagar' , Vista_pagar, name='cheque_pagar'),


        path('deposito/',DepositoView.as_view(), name='deposito_list'),
        path('deposito/new', DepositoNew.as_view(), name='deposito_new'),
        path('deposito/edit/<int:pk>',DepositoEdit.as_view(), name='deposito_edit'),

        path('deposito/imprimir-deposito/<str:f1>/<str:f2>' , imprimir_deposito_list, name="deposito_print_all"),
        path('detalle/deposito/<int:id>' , DepositoDetailView.as_view() , name='detail_deposito'),
        # path('cheque/estado/<int:id>', Cheque_inactivar, name='cheque_inactivar'),
        path('buscar/', search, name='bucsar'),
        path('cheques/no-entregados', reporte_che_entregados, name='che_pendiente_all'),

        path('che-entregado/',ChequeEntregadoView.as_view(), name='che_entregado_list'),
        path('che-entregado/new', ChequeEntregadoNew.as_view(), name='che_entregado_new'),
        path('che-rechazado/<int:id>', cheques_rechazados, name='che_rechazado'),

        path('cheque-rechazado/',ChequeRechazadoView.as_view(), name='cheque_rechazado_list'),
        path('che-rechazado/new', ChequeRechazadoNew.as_view(), name='cheque_rechazado_new'),
        path('cheques-recha-all', ChequeGeneratePendintesPDF.as_view(), name='cheques_recha_all'),

        path('prueba/', PDFPedidosHoy.as_view(), name='prueba_rechazo'),
        path('reporte/boleta-fecha/',deposito_filter, name = 'boleta_filter'),

        path('factura/',FacturaView.as_view(), name='factura_list'),
        path('factura/new', FacturaNew.as_view(), name='factura_new'),
        path('factura/edit/<int:pk>',FacturaEdit.as_view(), name='factura_edit'),

        path('abono/', Abono_FacturaView.as_view(), name='abono_factura_list'),
        path('abono/new', Abono_Fac.as_view(), name='abono_fac_new'),


]
