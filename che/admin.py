from django.contrib import admin
from .models import Cheque, Deposito

class ChequeAdmin(admin.ModelAdmin):
    list_display = ['no_cheque' , 'estado' ]

class DepositoAdmin(admin.ModelAdmin):
    {(
    
    )}




admin.site.register(Cheque, ChequeAdmin)
admin.site.register(Deposito, DepositoAdmin)
