#coding:utf-8
from django import forms

class RegisterForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField(required = False)
    phone = forms.IntegerField()
    password = forms.CharField(widget=forms.PasswordInput)
    address_name = forms.CharField(required = False)
    
class PictureForm(forms.Form):  
    headphoto = forms.ImageField()  
    user_id = forms.IntegerField(required = False)
    
class PersonalTailorForm(forms.Form):
    city = forms.CharField()
    begin_date = forms.IntegerField()
    end_date = forms.IntegerField()
    need = forms.CharField(required = False)
    user_id = forms.IntegerField(required = False)
    phone = forms.CharField()
    
    