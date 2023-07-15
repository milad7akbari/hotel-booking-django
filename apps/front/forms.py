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

class registerUser(forms.ModelForm):

    def clean(self):
        username = self.cleaned_data['username']
        if len(username) == 10:
            username = '09' + username[1:]
        email = self.cleaned_data['email']
        user = User.objects.filter(Q(username=username) | Q(email=email))
        errors_flag = 0
        if len(username) == 11 or len(username) == 10:
            regex = r'\b^(\+98|0)?9\d{9}$\b'
            if not re.fullmatch(regex, username):
                self.errors['username'] = _('موبایل اشتباه است!')
                errors_flag = 1
            chk = user.filter(username=username).first()

            if chk is not None:
                self.errors['username'] = _('موبایل وجود دارد!')
                errors_flag = 1
        else:
            self.errors['username'] = _('موبایل اشتباه است!')

        if len(email) > 0:
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if not re.fullmatch(regex, email):
                self.errors['email'] = _('ایمیل اشتباه است!')
                errors_flag = 1
            else:
                chk = user.filter(email=email).first()
                if chk is not None:
                    errors_flag = 1
                    self.errors['email'] = _('ایمیل وجود دارد!')
        else:
            self.errors['email'] = _('ایمیل اشتباه است!')
            errors_flag = 1

        if errors_flag == 1:
            self.errors['err'] = 1

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.NumberInput(attrs={"class": ' border-radius-5 fw-bolder align-left dir-ltr w-100',
                                               "placeholder": _('موبایل')}),
            'email': forms.EmailInput(attrs={"class": ' border-radius-5 fw-bolder align-left dir-ltr w-100',
                                             "placeholder": _('ایمیل')}),
            'password': forms.PasswordInput(attrs={"class": ' border-radius-5 fw-bolder dir-ltr align-left w-100',
                                                   "placeholder": _('پسورد')}),
        }
        labels = {
            'username': _('موبایل'),
            'email': _('ایمیل'),
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
