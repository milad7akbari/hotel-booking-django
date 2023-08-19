import re

from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from apps.base.models import User
from apps.front.models import  Order, Cart_cart_rule, Cart_guest


class forgotPasswordForm(forms.Form):
    username_email = forms.CharField(required=True, widget=forms.TextInput(
        attrs={"class": 'borderRadiusFPI fw-bolder align-left dir-ltr w-100'}), label=_('موبایل یا ایمیل'))


class loginUserForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={"class": 'borderRadiusFPI align-left dir-ltr w-100'}), label=_('موبایل یا ایمیل'))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={"class": 'borderRadiusFPI align-left dir-ltr w-100'}), label=_('پسورد'))


class trackingForm(forms.Form):
    reference = forms.CharField(required=True, widget=forms.TextInput(
        attrs={"class": 'border-radius-15 align-left dir-ltr w-100'}), label=_('رفرنس'))
    username = forms.CharField(required=True, widget=forms.NumberInput(
        attrs={"class": 'border-radius-15 align-left dir-ltr w-100'}), label=_('موبایل'))


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
        self.cleaned_data['username'] = username
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
        errors_flag = 0
        username = self.cleaned_data['username']
        firstname = self.cleaned_data['first_name']
        lastname = self.cleaned_data['last_name']
        email = self.cleaned_data['email']
        if len(email) > 0:
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if not re.fullmatch(regex, email):
                self.errors['email'] = _('ایمیل اشتباه است!')
                errors_flag = 1
            else:
                chk = User.objects.filter(Q(email=email)).first()
                if chk is not None:
                    errors_flag = 1
                    self.errors['email'] = _('ایمیل وجود دارد!')
        else:
            self.errors['email'] = _('ایمیل اشتباه است!')
            errors_flag = 1
        if len(firstname) < 2:
            self.errors['first_name'] = _('نام اشتباه است!')
            errors_flag = 1
        if len(lastname) < 2:
            self.errors['last_name'] = _('نام خانوادگی اشتباه است!')
            errors_flag = 1
        if len(username) == 10:
            username = '09' + username[1:]
        self.cleaned_data['username'] = username
        user = User.objects.filter(Q(username=username))
        if len(username) == 11 or len(username) == 10:
            regex = r'\b^(\+98|0)?9\d{9}$\b'
            if not re.fullmatch(regex, username):
                self.errors['username'] = _('موبایل اشتباه است!')
                errors_flag = 1
            chk = user.filter(username=username).first()

            if chk is not None:
                self.errors['username'] = _('موبایل وجود دارد لاگین کنید!')
                errors_flag = 1
        else:
            self.errors['username'] = _('موبایل اشتباه است!')
            errors_flag = 1

        if errors_flag == 1:
            self.errors['err'] = 1

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={"class": ' fs-14 py-1 w-100', "placeholder": _('نام')}),
            'last_name': forms.TextInput(attrs={"class": ' fs-14 py-1 w-100', "placeholder": _('نام خانوادگی')}),
            'username': forms.NumberInput(attrs={"class": ' fs-14 py-1 w-100', "placeholder": _('موبایل')}),
            'email': forms.EmailInput(attrs={"class": ' fs-14 py-1 w-100', "placeholder": _('ایمیل')}),
        }
        labels = {
            'first_name': _('نام'),
            'last_name': _('نام خانوادگی'),
            'username': _('موبایل'),
            'email': _('ایمیل'),
        }


class registerGuestFromReservationForm(forms.ModelForm):
    def clean(self):
        errors_flag = 0
        nationality = self.cleaned_data['nationality']
        mobile = self.cleaned_data['mobile']
        fullname = self.cleaned_data['fullname']

        if len(fullname) < 5:
            self.errors['fullname'] = _('نام کامل اشتباه است!')
            errors_flag = 1
        if nationality > 2 or nationality < 1:
            self.errors['nationality'] = _('ملیت اشتباه است!')
            errors_flag = 1
        if len(mobile) == 10:
            mobile = '09' + mobile[1:]
        if len(mobile) == 11 or len(mobile) == 10:
            regex = r'\b^(\+98|0)?9\d{9}$\b'
            if not re.fullmatch(regex, mobile):
                self.errors['mobile'] = _('موبایل اشتباه است!')
                errors_flag = 1
        else:
            self.errors['mobile'] = _('موبایل اشتباه است!')
            errors_flag = 1

        if errors_flag == 1:
            self.errors['err'] = 1

    class Meta:
        model = Cart_guest
        fields = ['fullname', 'mobile', 'nationality']
        CHOICES = (
            ('1', _('ایرانی')),
            ('2', _('غیر ایرانی')),
        )
        widgets = {
            'fullname': forms.TextInput(attrs={"class": ' fs-14 py-1 w-100',
                                                   "placeholder": _('نام کامل')}),
            'mobile': forms.NumberInput(attrs={"class": ' fs-14 py-1 w-100',
                                                  "placeholder": _('تلفن')}),
            'username': forms.Select(choices=CHOICES,attrs={"class": ' fs-14 py-1 w-100',
                                                 "placeholder": _('ملیت')}),
        }
        labels = {
            'fullname': _('نام کامل'),
            'mobile': _('تلفن'),
            'nationality': _('ملیت'),
        }

class placeOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['has_invoice', 'agree_rule']
        widgets = {
            'has_invoice': forms.CheckboxInput(attrs={"class": ' fs-14 py-1 w-100', 'autocomplete':'off' , 'checked':'false' ,
                                                   "placeholder": _('دریافت فاکتور رسمی')}),
            'agree_rule': forms.CheckboxInput(attrs={"class": ' fs-14 py-1 w-100', 'autocomplete':'off','checked':'false',
                                                   "placeholder": _('دریافت فاکتور رسمی')}),
        }
        labels = {
            'has_invoice': _('دریافت فاکتور رسمی'),
            'agree_rule': _(' با پرداخت سفارش با قوانین رزرو اینترنتی هتل تیک و قوانین لغو رزرو هتل موافقت می کنم!'),
        }
