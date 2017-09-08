from django import forms
from django.forms import ModelForm
from django.db import models
from trade_savante.models import TradeItem


class signInForm(forms.Form):
    username = forms.CharField(max_length = 50)
    password = forms.CharField(widget=forms.PasswordInput)
