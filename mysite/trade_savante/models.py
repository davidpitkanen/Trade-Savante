from __future__ import unicode_literals
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms

Housing = 'housing'
Electronics = 'electronics'
Auto = 'automotive'
Bike = 'bike'
Leisure = 'leisure'
Sports = 'sports'
Fashion = 'fashion'
Books = 'bike'
Money = 'money'
Services = 'services'
notapplicable = 'na'


category_choices = (
    (notapplicable,'Not applicable'),
    (Housing, 'Housing'),
    (Electronics, 'Electronics'),
    (Auto, 'Automotive'),
    (Bike, 'Bike'),
    (Leisure, 'Leisure'),
    (Sports, 'Sports'),
    (Fashion, 'Fashion'),
    (Books, 'Books'),
    (Money, 'Money'),
    (Services, "Services"),
)

class sequenceManager(models.Manager):

    def with_counts(self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""SELECT MAX(t.id) as max_id, MIN(t.id) as min_id, count(*) as chain_length FROM trade_savante_TradeSequence t Group by t.sequenceid""")
        result_list = {"max_name": [], "min_name": [], "chain_length": []}
        #for row in cursor.fetchall():
        #    #result_list["name"].append(row[0])
        #    result_list["max_name"].append(TradeSequence.objects.get(id=row[1]).tradeConnection.name)
        #    result_list["min_name"].append(TradeSequence.objects.get(id=row[2]).tradeConnection.name)
        #    result_list["chain_length"].append(row[3])
        return 1 #zip(result_list["max_name"], result_list["min_name"], result_list["chain_length"])

    #def get_wanted_items(self, user_id):
    #    from django.db import connection
    #    cursor = connection.cursor()
    #    cursor.execute("""SELECT DISTINCT t.id FROM trade_savante_IndividualTrades as p JOIN trade_savante_TradeItem as t ON
    #    p.askerItem = t.id JOIN trade_savante_User as u on t.owner = u.id WHERE u.id = %s""" % (user_id))
    #    # I want to return a list of 
    #    for row in cursor.fetchall():
    #        result
      

class Address(models.Model):
    city = models.CharField(max_length=100, null=True) 
    state = models.CharField(max_length=2, null=True) 
    country = models.CharField(max_length=2, null=True) 
    postal_code = models.CharField(max_length=16, null=True) 
	
class TradeItem(models.Model):
    name = models.CharField(max_length=140, null=True)
    price = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    category = models.CharField(max_length=20, choices=category_choices) # foreignKey
    description = models.TextField(null=True)
    asking_for = models.TextField(null=True)
    active_start_date = models.DateField(auto_now_add=True, null=True) # probably just date is fine.
    owner = models.ForeignKey(User,on_delete=models.CASCADE, null=True) # foreign Key
    been_traded = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='tradesavante', null=True, blank=True)

class SearchKeywords(models.Model):
    key_word = models.TextField(null=True)
    itemsearch = models.ForeignKey(TradeItem, on_delete=models.CASCADE, null=False)

class Message(models.Model):
     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
     reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reciever")
     msg_title = models.CharField(max_length=140, null=True)
     msg_content = models.TextField(null=True)
     created_at = models.DateField(auto_now_add=True, null=True)

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
    sequenceid = models.IntegerField(null=False,default=1)
    objects = sequenceManager()

class SearchForm(forms.Form):
    search = forms.CharField(max_length = 50)
    category = forms.ChoiceField(choices=category_choices)
    min_price = forms.DecimalField(max_digits=11, decimal_places=2, required=False)
    max_price = forms.DecimalField(max_digits=11, decimal_places=2, required=False)

class TradeItemForm(ModelForm):
    class Meta:
        model = TradeItem
        fields = ['name','price','category', 'description', 'asking_for', 'image']

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['msg_title','msg_content']

class KeyWordForm(ModelForm):
    class Meta:
        model = SearchKeywords
        fields = ['key_word']