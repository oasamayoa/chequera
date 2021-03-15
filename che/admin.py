from django.contrib import admin
from .models import Cheque, Deposito, Factura

class ChequeAdmin(admin.ModelAdmin):
    list_display = ['no_cheque' , 'estado' ]

class DepositoAdmin(admin.ModelAdmin):
    {(

    )}

class FacturaAdmin(admin.ModelAdmin):
    {(
    
    )}



admin.site.register(Cheque, ChequeAdmin)
admin.site.register(Deposito, DepositoAdmin)
admin.site.register(Factura, FacturaAdmin)
