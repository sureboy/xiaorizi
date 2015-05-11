#coding:utf-8
from django import forms

class orderForm(forms.Form):
    number = forms.IntegerField(min_value=1, label=u'数量')
    user_name = forms.CharField(min_length=2,max_length=20,label=u'姓名')
    email = forms.EmailField(required=False,label=u'您的邮箱')
    mobilphone = forms.IntegerField(label=u'手机')
    phone = forms.IntegerField(required=False,label=u'电话')
    address = forms.CharField(label=u'收货地址')
    payMode = forms.ChoiceField(choices=[('1',u'支付宝'),('2',u'银行转账')],label=u'支付方式')
    message = forms.CharField(required=False,widget=forms.Textarea,label=u'留言')
    '''
    def clean_message(self):
        message = self.cleaned_data['message']
        num_words = len(message.split())
        if num_words < 4:
            raise forms.ValidationError("Not enough words!")
        return message'''
    
class messageForm(forms.Form):
    user_name = forms.CharField(min_length=2,max_length=20)
    email = forms.EmailField(required=False)
    telphone = forms.IntegerField()
    phone = forms.IntegerField(required=False)
    message = forms.CharField()