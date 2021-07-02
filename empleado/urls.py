from django.urls import path
from empleado.views import EmpleadoView, FarmaciaView, FarmaciaNew

urlpatterns = [
    path('empleado/', EmpleadoView.as_view(), name='empleado_list'),
    path('farmacia', FarmaciaView.as_view(), name='farmacia_list' ),
    path('farmacia-new', FarmaciaNew.as_view(), name='farmacia_new')

]
