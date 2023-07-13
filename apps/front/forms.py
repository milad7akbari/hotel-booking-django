import re

from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from apps.base.models import User

class forgotPasswordForm(forms.Form):
    username_email = forms.CharField(required=True, widget=forms.TextInput(
        attrs={"class": 'borderRadiusFPI fw-bolder align-left dir-ltr w-100'}), label=_('موبایل یا ایمیل'))


class loginUserForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={"class": 'borderRadiusFPI fw-bolder align-left dir-ltr w-100'}), label=_('موبایل یا ایمیل'))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={"class": 'borderRadiusFPI fw-bolder align-left dir-ltr w-100'}), label=_('پسورد'))


class forgotPasswordConfirmForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password']
        widgets = {
            'password': forms.PasswordInput(attrs={"class": 'border-radius-5 fw-bolder dir-ltr align-left w-100',
                                                   "placeholder": _('پسورد')}),
        }
        labels = {
            'password': _('پسورد'),
        }




class registerUserFromReservationForm(forms.ModelForm):

    def clean(self):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        user = User.objects.filter(Q(username=username) | Q(email=email))
        errors_flag = 0

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'first_name': forms.NumberInput(attrs={"class": ' fs-14 py-1 w-100',
                                                   "placeholder": _('نام')}),
            'last_name': forms.NumberInput(attrs={"class": ' fs-14 py-1 w-100',
                                                  "placeholder": _('نام خانوادگی')}),
            'username': forms.NumberInput(attrs={"class": ' fs-14 py-1 w-100',
                                               "placeholder": _('موبایل')}),
            'email': forms.EmailInput(attrs={"class": ' fs-14 py-1 w-100',
                                             "placeholder": _('ایمیل')}),
        }
        labels = {
            'first_name': _('نام'),
            'last_name': _('نام خانوادگی'),
            'username': _('موبایل'),
            'email': _('ایمیل'),
        }


class registerGuestFromReservationForm(forms.ModelForm):

    def clean(self):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        username = self.cleaned_data.get('username')
        user = User.objects.filter(Q(username=username))
        errors_flag = 0

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        widgets = {
            'first_name': forms.NumberInput(attrs={"class": ' fs-14 py-1 w-100',
                                                   "placeholder": _('نام')}),
            'last_name': forms.NumberInput(attrs={"class": ' fs-14 py-1 w-100',
                                                  "placeholder": _('نام خانوادگی')}),
            'username': forms.NumberInput(attrs={"class": ' fs-14 py-1 w-100',
                                                 "placeholder": _('کدملی')}),
        }
        labels = {
            'first_name': _('نام'),
            'last_name': _('نام خانوادگی'),
            'username': _('کدملی'),
        }
