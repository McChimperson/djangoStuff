from django.contrib import admin

# Register your models here.
from .models import Transactions, Reporters

class TransactionsAdmin(admin.ModelAdmin):
    class Meta:
        model = Transactions

        
class ReportersAdmin(admin.ModelAdmin):
    class Meta:
        model = Reporters
        
admin.site.register(Reporters)        
admin.site.register(Transactions)