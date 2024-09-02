from django.contrib import admin
from .models import *

# Register your models here.
class MutualFundAdmin(admin.ModelAdmin):
    list_display = ('app', 'fund_name', 'fund_type', 'investment_amount','units_purchased','returns','cagr','xirr')
    search_fields = ('app','fund_name')
    list_filter = ('app','fund_name')

admin.site.register(MutualFund, MutualFundAdmin)
admin.site.register(Investments)
admin.site.register(AllAccount)
admin.site.register(StockPortfolio)

