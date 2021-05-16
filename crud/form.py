from django.forms import ModelForm
from django.core import validators
from django import forms
from .models import *


class SupplierForm(ModelForm):

    class Meta:
        model = Supplier
        fields=['name','Number','city','resources','email','description']
        name=forms.CharField(max_length=100)
        Number=forms.IntegerField()
        city=forms.ModelMultipleChoiceField(queryset=City.objects.all())
        resources=forms.ModelMultipleChoiceField(queryset=Resources.objects.all())
        widgets ={
        'name': forms.TextInput(attrs={'class':'form-control'}),
        'Number': forms.TextInput(attrs={'maxlength':'10', 'class':'phone'}),
        'city': forms.CheckboxSelectMultiple(attrs={'type':'checkbox'}),
        'resources': forms.CheckboxSelectMultiple(attrs={'type':'checkbox'}),
        'email': forms.EmailInput(attrs={'class':'form-control'}),
        'description':forms.Textarea(attrs={'class':'form-control'})
        }