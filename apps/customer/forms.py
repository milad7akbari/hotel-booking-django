import re

from django import forms
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _

from apps.base.models import User


class editUser(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(editUser, self).__init__(*args, **kwargs)
    def clean(self):
        email = self.cleaned_data['email']
        if len(email) > 0:
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if not re.fullmatch(regex, email):
                self.errors['email'] = _('ایمیل اشتباه است!')
            else:
                if self.user.email != email:
                    chk = User.objects.filter(email=email).first()
                    if chk is not None:
                        self.errors['email'] = _('ایمیل وجود دارد!')
        else:
            self.errors['email'] = _('ایمیل اشتباه است!')

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={"class": ' border-radius-5',
                                                 "placeholder": _('نام')}),
            'last_name': forms.TextInput(attrs={"class": ' border-radius-5',
                                                 "placeholder": _('نام خانوادگی')}),
            'email': forms.EmailInput(attrs={"class": ' border-radius-5',
                                             "placeholder": _('ایمیل')}),
            'password': forms.PasswordInput(attrs={"class": ' border-radius-5 ',
                                                   "placeholder": _('پسورد')}),
        }
        labels = {
            'first_name': _('نام'),
            'last_name': _('نام خانوادگی'),
            'email': _('ایمیل'),
            'password': _('پسورد'),
        }
class editUserPassword(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(editUserPassword, self).__init__(*args, **kwargs)
    def clean(self):
        password = self.cleaned_data['password']
        if len(password) <= 1:
            self.errors['email'] = _('پسورد اشتباه است حداقل 6 کاراکتر!')

    class Meta:
        model = User
        fields = ['password']
        widgets = {
            'password': forms.PasswordInput(attrs={"class": ' border-radius-5 ',
                                                   "placeholder": _('پسورد')}),
        }
        labels = {
            'password': _('پسورد'),
        }
