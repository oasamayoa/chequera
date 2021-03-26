from django.urls import path
from empleado.views import EmpleadoView

urlpatterns = [
    path('empleado/', EmpleadoView.as_view(), name='empleado_list')

]
