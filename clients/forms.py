from django import forms
from django.core.exceptions import ValidationError
from contextlib import suppress

from .models import (
    RegistrationOrder
)


class CustomRegOrderForm(forms.ModelForm):
    login    = forms.CharField(required=False)
    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False
    )

    class Meta:
        model = RegistrationOrder
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean() 

        registration_order = self.cleaned_data
        if not registration_order.get('status') or registration_order.get('status') != 'registered':
            return
                   
        if not self.cleaned_data.get('login'):
            self.add_error('login', 'Не указан логин персонального менеджера')
        
        if not self.cleaned_data.get('password'):
            self.add_error('password', 'Не указан пароль персонального менеджера')


class RegForm(forms.ModelForm):

    class Meta:
        model = RegistrationOrder
        fields = ('name', 'organization', 'inn', 'phone', 'email')
        labels = {
            'name'                  : 'Ваше имя',
            'organization'          : 'Организация',
            'inn'                   : 'ИНН',
            'phone'                 : 'Номер телефона',
            'email'                 : 'e-mail',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control default-input reg-field-layout'


class LoginForm(forms.Form):
    login = forms.CharField(
        label='ИНН',
        widget=forms.TextInput(
            attrs={'class': 'form-control default-input reg-field-layout', 'placeholder': 'ИНН / email'}
        )
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control default-input reg-field-layout', 'placeholder': 'Пароль'}
        )
    )
    fields = ['login', 'password']


class ChangePassForm(forms.Form):
    login = forms.CharField(
        label='ИНН',
        widget=forms.TextInput(
            attrs={'class': 'form-control default-input reg-field-layout', 'placeholder': 'ИНН'}
        )
    )
    old_pass = forms.CharField(
        label='Старый пароль',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control default-input reg-field-layout', 'placeholder': ''}
        )
    )
    new_pass = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control default-input reg-field-layout', 'placeholder': ''}
        )
    )
    repeat_pass = forms.CharField(
        label='Повторите пароль еще раз',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control default-input reg-field-layout', 'placeholder': ''}
        )
    )
    fields = ['login', 'old_pass', 'new_pass', 'repeat_pass']

    def clean_login(self):
        value = self.cleaned_data['login']  
        if not RegistrationOrder.objects.filter(inn=value).exists():
            raise ValidationError('Клиент с таким ИНН не существует')
        return value
    
    def clean_repeat_pass(self):
        new_pass = self.cleaned_data['new_pass']
        repeat_pass = self.cleaned_data['repeat_pass']
        if not new_pass == repeat_pass:
            raise ValidationError('Пароли не совпадают')
        return repeat_pass
