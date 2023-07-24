from django import forms
from django.utils.translation import gettext_lazy as _

from apps.hotel.models import Reviews, Hotel


class reviewsForm(forms.ModelForm):
    
    def clean(self):
        errors_flag = 0
        hotel_ref = self.cleaned_data['hotel_ref']
        hotel = Hotel.objects.filter(reference=hotel_ref).first()
        if hotel is None:
            self.errors['title'] = _('هتل یافت نشد')
            errors_flag = 1
        hotel = Reviews.objects.filter(hotel_id=hotel.pk, ).first()

        stars = self.cleaned_data['stars']
        title = self.cleaned_data['title']
        short_desc = self.cleaned_data['short_desc']
        if stars < 1 or stars > 5 :
            self.errors['stars'] = _('امتیاز را انتخاب کنید!')
            errors_flag = 1
        if len(title) <= 10:
            self.errors['title'] = _('موضوع کمتر از ده کاراکتر است')
            errors_flag = 1

        if len(title) <= 10:
            self.errors['title'] = _('موضوع کمتر از ده کاراکتر است')
            errors_flag = 1

        if len(short_desc) <= 10:
            self.errors['short_desc'] = _('توضیحات کمتر از ده کاراکتر است')
            errors_flag = 1
        if errors_flag == 1:
            self.errors['err'] = 1
    class Meta:
        model = Reviews
        fields = ['stars', 'title','short_desc','desc_good','desc_bad']
        widgets = {
            'stars': forms.HiddenInput(attrs={"class": ' border-radius-5 fs-13  w-100',
                                               "placeholder": _('ستاره')}),
            'title': forms.TextInput(attrs={"class": ' border-radius-5 fs-13 w-100',
                                               "placeholder": _('عنوان')}),
            'short_desc': forms.Textarea(attrs={"class": ' border-radius-5 fs-13 w-100',
                                             "placeholder": _('توضیحات'), 'rows': 3}),
            'desc_good': forms.Textarea(attrs={"class": ' border-radius-5 text-success fs-13 w-100',
                                             "placeholder": _('نکات مثبت'), 'rows': 3}),
            'desc_bad': forms.Textarea(attrs={"class": ' border-radius-5 text-danger fs-13 w-100',
                                             "placeholder": _('نکات منفی'), 'rows': 3}),
        }
        labels = {
            'stars': _('ستاره'),
            'title': _('عنوان'),
            'short_desc': _('توضیحات'),
            'desc_good': _('نکات مثبت'),
            'desc_bad': _('نکات منفی'),
        }
