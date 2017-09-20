from django.contrib import admin
from trade_savante.models import TradeItem, IndividualTrades, Message
# Register your models here.

admin.site.register(TradeItem)
admin.site.register(IndividualTrades)
admin.site.register(Message)