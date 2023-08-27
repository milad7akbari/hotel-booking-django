import os
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


def file_category(self, filename):
    ext = filename.split('.')[-1]
    if self.pk is None:
        pk = 1
    else:
        pk = self.pk + 1
    filename = "%s.%s" % (str(pk), ext)
    return os.path.join('media/slider/images/', filename)


def file_city(self, filename):
    ext = filename.split('.')[-1]
    if self.pk is None:
        pk = 1
    else:
        pk = self.pk + 1
    filename = "%s.%s" % (str(pk), ext)
    return os.path.join('media/city/images/', filename)


class Slider(models.Model):
    def validate_image(self):
        filesize = self.file.size
        megabyte_limit = 1
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError(_("حداکثر حجم فایل %sMB") % str(megabyte_limit))

    file = models.ImageField(upload_to=file_category, blank=True, null=True, validators=[validate_image],
                             help_text=_("حداکثر حجم فایل 1MB"))
    active = models.SmallIntegerField(null=False, default=0, verbose_name=_('فعال'))
    date_upd = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ آپدیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('تاریخ ایجاد'))

    def img_preview(self):
        return format_html('<img style="width: 100px;" src="{}" />'.format(self.file.url))

    class Meta:
        verbose_name_plural = _('اسلایدر')
        verbose_name = _('اسلایدر')

    def __str__(self):
        return self.pk


class Forgot_password(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0, null=True, verbose_name=_('مشتری'))
    token = models.CharField(max_length=255, default=0, null=True, verbose_name=_('توکن'))
    status = models.SmallIntegerField(null=False, default=0, verbose_name=_('وضعیت'))
    date_upd = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ آپدیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('تاریخ ایجاد'))

    class Meta:
        verbose_name_plural = _('فراموشی پسورد')
        verbose_name = _('فراموشی پسورد')

    def __str__(self):
        return self.user.first_name

    def __unicode__(self):
        return self.user.first_name


class Footer(models.Model):
    PTYPE = (('postal_code', 'کد پستی'), ('phone', 'تلفن'), ('email', 'ایمبل'), ('instagram', 'اینستاگرام'),
             ('whatsapp', 'واتس اپ'), ('telegram', 'تلگرام'),)
    name = models.CharField(choices=PTYPE, null=True, max_length=255, verbose_name=_('نام'))
    value = models.CharField(null=True, max_length=255, verbose_name=_('مقدار'))
    date_upd = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ آپدیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('تاریخ ایجاد'))

    class Meta:
        verbose_name_plural = _('فوتر')
        verbose_name = _('فوتر')

    def __str__(self):
        return self.value

    def __unicode__(self):
        return self.value


class Provinces(models.Model):
    name = models.CharField(null=True, max_length=128, verbose_name=_('نام استان'))
    latitude = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=8, verbose_name=_('عرض جغرافیایی'))
    longitude = models.DecimalField(null=True, blank=True, max_digits=11, decimal_places=8, verbose_name=_('طول جغرافیایی'))
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('تاریخ ایجاد'))

    def __unicode__(self):
        return str(self.name)

    class Meta:
        verbose_name = _('استان')
        verbose_name_plural = _('استان')

    def __str__(self):
        return str(self.name)

class Sms_log(models.Model):
    code = models.CharField(null=True, max_length=128, verbose_name=_('کد'))
    receiver = models.CharField(null=True, max_length=128, verbose_name=_('دریافت کننده'))
    type = models.CharField(null=True, max_length=128, verbose_name=_('نوع'))
    message = models.TextField(null=True, verbose_name=_('متن'))
    status_code = models.SmallIntegerField(null=True, verbose_name=_('کد برگشتی'))
    date_add = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('تاریخ ایجاد'))

    def __unicode__(self):
        return str(self.code)

    class Meta:
        verbose_name = _('پیامک ها')
        verbose_name_plural = _('پیامک ها')

    def __str__(self):
        return str(self.code)


class Cities(models.Model):
    def validate_image(self):
        filesize = self.file.size
        megabyte_limit = 1
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError(_("حداکثر حجم فایل %MB") % str(megabyte_limit))

    provinces = models.ForeignKey(Provinces, default=None, on_delete=models.CASCADE, verbose_name=_('استان'))
    name = models.CharField(null=True, max_length=128, verbose_name=_('نام شهر'))
    file = models.ImageField(upload_to=file_city, null=True, blank=True, validators=[validate_image],
                             help_text=_('Maximum file size allowed is 1Mb'), verbose_name=_('فایل'))
    latitude = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=8, verbose_name=_('عرض جغرافیایی'))
    longitude = models.DecimalField(null=True, blank=True, max_digits=11, decimal_places=8, verbose_name=_('طول جغرافیایی'))
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('تاریخ ایجاد'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('شهر')
        verbose_name_plural = _('شهر')

    def __str__(self):
        return self.name


class Meta(models.Model):
    PTYPE = (('hotels', 'همه هتل ها'), ('home_page', 'صفحه اصلی'), ('about_us_page', 'درباره ما'),
             ('general_policy_page', 'قوانین و مقررات'), ('cart_page', 'سبد خرید'),)
    page_name = models.CharField(choices=PTYPE, max_length=255, blank=True, verbose_name=_('نام صفحه'))
    title = models.CharField(max_length=255, blank=True, verbose_name=_('عنوان'))
    description = models.TextField(blank=True, verbose_name=_('توضیحات'))
    keywords = models.TextField(blank=True, help_text="some tag, hoteltik, international, etc...", verbose_name=_('کلید واژه'))
    date_upd = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ آپدیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('تاریخ ایجاد'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = _('متا')
        verbose_name = _('متا')

    def __unicode__(self):
        return self.title


class Pages(models.Model):
    PTYPE = (('about-us', 'درباره ما'), ('general_policy_page', 'قوانین و مقررات'),)
    page_name = models.CharField(choices=PTYPE, max_length=255, blank=True, verbose_name=_('نام صفحه'))
    description = models.TextField(blank=True, verbose_name=_('توضیحات'))
    date_upd = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ آپدیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('تاریخ ایجاد'))

    def __str__(self):
        return self.page_name

    class Meta:
        verbose_name_plural = _('صفحه ها')
        verbose_name = _('صفحه ها')

    def __unicode__(self):
        return self.page_name


class Configuration(models.Model):
    PTYPE = (('new', 'شرط برای هتل جدید'),)
    name = models.CharField(choices=PTYPE, max_length=255, blank=True, verbose_name=_('نام'))
    value = models.CharField(max_length=255, blank=True, verbose_name=_('مقدار'))
    date_upd = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ آپدیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('تاریخ ایجاد'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('کانفیگ')
        verbose_name = _('کانفیگ')

    def __unicode__(self):
        return self.name
