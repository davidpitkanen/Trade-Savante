from __future__ import unicode_literals
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

Bike = 'bike'
Leisure = 'leisure'
Sports = 'sports'
Fashion = 'fashion'
Books = 'bike'
notapplicable = 'na'


category_choices = (
    (Bike, 'Bike'),
    (Leisure, 'Leisure'),
    (Sports, 'Sports'),
    (Fashion, 'Fashion'),
    (Books, 'Books'),
	(notapplicable,'Not applicable'),
)


class Address(models.Model):
    city = models.CharField(max_length=100, null=True) #
    state = models.CharField(max_length=2, null=True) #
    country = models.CharField(max_length=2, null=True) #
    postal_code = models.CharField(max_length=16, null=True) # 
	
class TradeItem(models.Model):
    name = models.CharField(max_length=140, null=True)
    price = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    category = models.CharField(max_length=20, choices=category_choices) # foreignKey
    description = models.TextField(null=True)
    active_start_date = models.DateField(auto_now_add=True, null=True) # probably just date is fine.
    owner = models.ForeignKey(User,on_delete=models.CASCADE, null=True) # foreign Key
    been_traded = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='tradesavante', null=True, blank=True)
	
class IndividualTrades(models.Model):
    askerItem = models.ForeignKey(TradeItem, on_delete=models.CASCADE, related_name='askerItem', null=True)
    ownerItem = models.ForeignKey(TradeItem, on_delete=models.CASCADE, related_name='ownerItem', null=True)
    verifiedTrade = models.BooleanField(default=False) # boolean
    ownerAnswer = models.BooleanField(default=False) # not sure what this means?  

class TradeSequence(models.Model):
    linkNumber = models.IntegerField(null=False, default=0)
    tradeConnection = models.ForeignKey(IndividualTrades, on_delete=models.CASCADE, null=False)
    isClosed = models.BooleanField(default=False)
    sequencer = models.ForeignKey(User,on_delete=models.CASCADE, null=True)

class TradeItemForm(ModelForm):
    class Meta:
        model = TradeItem
        fields = ['name','price','category', 'description', 'image']