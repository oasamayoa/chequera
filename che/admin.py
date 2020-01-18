from django.contrib import admin
from .models import Cheque

class ChequeAdmin(admin.ModelAdmin):
    list_display = ['no_cheque' , 'estado' ]

admin.site.register(Cheque, ChequeAdmin)
