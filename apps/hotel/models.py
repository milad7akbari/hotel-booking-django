import os

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from urllib3 import request

from apps.base.models import Cities


def file(self, filename):
    ext = filename.split('.')[-1]
    if self.pk is None:
        pk = 1
    else:
        pk = self.pk + 1
    filename = "%s.%s" % (str(pk), ext)
    return os.path.join('media/hotel/files/', filename)


def file_room(self, filename):
    ext = filename.split('.')[-1]
    if self.pk is None:
        pk = 1
    else:
        pk = self.pk + 1
    filename = "%s.%s" % (str(pk), ext)
    return os.path.join('media/hotel/room/files/', filename)


class Hotel(models.Model):
    def save(self, *args, **kwargs):
        replacers = {'$', "/", "+", "="}
        ref = make_password(str(self.pk), salt="Argon2PasswordHasher", hasher="default")
        for r in replacers:
            ref = ref.replace(r, '')
        self.reference = ref[-7:]
        super(Hotel, self).save(*args, **kwargs)

    TYPE_STARS = ((1, '1'), (2, '2'), (4, '3'), (4, '4'), (5, '5'),)
    TYPE_TRUE = ((1, 'Yes'), (0, 'NO'),)
    TYPE_HOTEL = ((1, 'آنلاین'), (2, 'آفلاین'),)
    name = models.CharField(null=True, max_length=255, verbose_name=_("نام هتل"))
    reference = models.CharField(null=True, max_length=255, verbose_name=_("رفرنس"))
    long_desc = models.TextField(null=True, blank=True, verbose_name=_("توضیحات بلند"))
    short_desc = models.TextField(null=True, blank=True, verbose_name=_("توضیحات کوتاه"))
    rule_cancelable = models.TextField(null=True, blank=True, verbose_name=_("قوانین کنسل"))
    rule_enter = models.TextField(null=True, blank=True, verbose_name=_("قوانین ورود و خروج"))
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, verbose_name=_("شهر"))
    address = models.CharField(null=True, blank=True, max_length=255, verbose_name=_("آدرس"))
    latitude = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=8)
    longitude = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=8)
    phone_number = models.CharField(null=True, blank=True, max_length=255, verbose_name=_("شماره تلفن"))
    email = models.EmailField(null=True, blank=True, max_length=255, verbose_name=_("ایمیل"))
    number_rooms = models.SmallIntegerField(null=True, blank=True, default=0, verbose_name=_("تعداد اتاق ها"))
    number_floor = models.SmallIntegerField(null=True, blank=True, default=0, verbose_name=_("تعداد طبقه"))
    stars = models.PositiveSmallIntegerField(choices=TYPE_STARS, default=1, verbose_name=_("ستاره ها"))
    default_cover = models.ForeignKey('Cover', on_delete=models.CASCADE, null=True,
                                      verbose_name=_("عکس پیش فرض"))
    meta_keywords = models.CharField(default=None, null=True, blank=True, max_length=255,
                                     help_text="some tag, espinas, international, etc...", verbose_name=_("متا کیبورد"))
    has_early_check_in_out = models.SmallIntegerField(choices=TYPE_TRUE, blank=True, null=True, default=1,
                                                      verbose_name=_("دارای ورود و خروج زود هنگام"))
    type = models.SmallIntegerField(choices=TYPE_HOTEL, blank=True, null=True, default=1, verbose_name=_("نوع هتل"))
    has_breakfast = models.SmallIntegerField(choices=TYPE_TRUE, blank=True, null=True, default=1, verbose_name=_("دارای صبحانه"))
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=1, verbose_name=_("فعال"))
    upd_add = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ آپدیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('تاریخ ایجاد'))

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = _('هتل ها')
        verbose_name = _('هتل ها')

    def __unicode__(self):
        return 'Hotel'


class Images(models.Model):
    TYPE_TRUE = ((1, 'Yes'), (0, 'NO'),)

    def validate_image(self):
        filesize = self.file.size
        megabyte_limit = 1
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError(_("Max file size is %sMB") % str(megabyte_limit))

    file = models.ImageField(upload_to=file, null=False, default=None, validators=[validate_image],
                             help_text=_('Maximum file size allowed is 1Mb'))
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("نام هتل"))
    date_upd = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ آپدیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('تاریخ ایجاد'))

    def file_uploaded(self):
        ext = self.file.url.split('.')[-1].lower()
        valid_extensions = ['jpg', 'png', 'jpeg']
        if ext in valid_extensions:
            return format_html('<img style="width: 100px;" src="{}" />'.format(self.file.url))
        else:
            return format_html('<a href="{}">Click Me</a>'.format(self.file.url))

    class Meta:
        verbose_name_plural = _("عکس های هتل ها")
        verbose_name = _("عکس های هتل ها")

    def __str__(self):
        return str(self.pk)


class Cover(models.Model):
    TYPE_TRUE = ((1, 'Yes'), (0, 'NO'),)

    def validate_image(self):
        filesize = self.file.size
        megabyte_limit = 1
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError(_("Max file size is %sMB") % str(megabyte_limit))

    file = models.ImageField(upload_to=file, blank=True, null=True, validators=[validate_image],
                             help_text=_('Maximum file size allowed is 1Mb'))
    date_upd = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ آپدیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('تاریخ ایجاد'))

    def file_uploaded(self):
        ext = self.file.url.split('.')[-1].lower()
        valid_extensions = ['jpg', 'png', 'jpeg']
        if ext in valid_extensions:
            return format_html('<img style="width: 100px;" src="{}" />'.format(self.file.url))
        else:
            return format_html('<a href="{}">Click Me</a>'.format(self.file.url))

    class Meta:
        verbose_name_plural = _("کاور هتل ها")
        verbose_name = _("کاور هتل ها")

    def __str__(self):
        return str(self.pk)


class Facility(models.Model):
    TYPE_TRUE = ((1, 'Yes'), (0, 'NO'),)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("نام هتل"))
    title = models.CharField(null=True, max_length=255, verbose_name=_("عنوان"))
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=0, verbose_name=_("فعال"))
    date_upd = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ آپدیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('تاریخ ایجاد'))

    class Meta:
        verbose_name_plural = _("امکانات  هتل ها")
        verbose_name = _("امکانات  هتل ها")

    def __str__(self):
        return str(self.title)




class Extra_person_rate(models.Model):
    TYPE_TRUE = ((1, 'Yes'), (0, 'NO'),)
    hotel = models.OneToOneField(Hotel, on_delete=models.SET_NULL, blank=True, null=True,
                                 related_name='extra_person_rate', verbose_name=_("نام هتل"))
    rate = models.DecimalField(null=True, max_digits=12, decimal_places=2, default=0, verbose_name=_("قیمت"))
    date_upd = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ آپدیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('تاریخ ایجاد'))

    class Meta:
        verbose_name_plural = _("نفر اضافه")
        verbose_name = _("نفر اضافه")

    def __str__(self):
        return str(self.hotel.name)


class Breakfast_rate(models.Model):
    TYPE_TRUE = ((1, 'Yes'), (0, 'NO'),)
    hotel = models.OneToOneField(Hotel, on_delete=models.SET_NULL, blank=True, null=True, related_name='breakfast_rate',
                                 verbose_name=_("نام هتل"))
    rate = models.DecimalField(null=True, max_digits=12, decimal_places=2, default=0, verbose_name=_("قیمت"))
    date_upd = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ آپدیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('تاریخ ایجاد'))

    class Meta:
        verbose_name_plural = _("نرخ صبحانه")
        verbose_name = _("نرخ صبحانه")

    def __str__(self):
        return str(self.hotel.name)


class Check_in_out_rate(models.Model):
    TYPE_TRUE = ((1, 'Yes'), (0, 'NO'),)
    hotel = models.OneToOneField(Hotel, on_delete=models.SET_NULL, blank=True, null=True,
                                 related_name='check_in_out_rate', verbose_name=_("نام هتل"))
    rate = models.DecimalField(null=True, max_digits=12, decimal_places=2, default=0, verbose_name=_("قیمت"))
    date_upd = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ آپدیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('تاریخ ایجاد'))

    class Meta:
        verbose_name_plural = _("نرخ ورود و خروج")
        verbose_name = _("نرخ ورود و خروج")

    def __str__(self):
        return str(self.hotel.name)


class Close_spots(models.Model):
    TYPE_TRUE = ((1, 'Yes'), (0, 'NO'),)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("نام هتل"))
    short_desc = models.CharField(null=True, max_length=512, verbose_name=_("توضیحات کوتاه"))
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=0, verbose_name=_("فعال"))
    date_upd = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ آپدیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('تاریخ ایجاد'))

    class Meta:
        verbose_name_plural = _("مکان های نزدیک")
        verbose_name = _("مکان های نزدیک")

    def __str__(self):
        return str(self.short_desc)


class Room_cover(models.Model):
    TYPE_TRUE = ((1, 'Yes'), (0, 'NO'),)

    def validate_image(self):
        filesize = self.file.size
        megabyte_limit = 1
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError(_("Max file size is %sMB") % str(megabyte_limit))

    file = models.ImageField(upload_to=file_room, blank=True, null=True, validators=[validate_image],
                             help_text=_('Maximum file size allowed is 1Mb'))
    date_upd = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ آپدیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('تاریخ ایجاد'))

    def file_uploaded(self):
        ext = self.file.url.split('.')[-1].lower()
        valid_extensions = ['jpg', 'png', 'jpeg']
        if ext in valid_extensions:
            return format_html('<img style="width: 100px;" src="{}" />'.format(self.file.url))
        else:
            return format_html('<a href="{}">Click Me</a>'.format(self.file.url))

    class Meta:
        verbose_name_plural = _("کاور اتاق ها")
        verbose_name = _("کاور اتاق ها")

    def __str__(self):
        return str(self.pk)


class Room(models.Model):
    TYPE_TRUE = ((1, 'Yes'), (0, 'NO'),)
    title = models.CharField(null=True, max_length=255, verbose_name=_("عنوان"))
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, verbose_name=_("نام هتل"))
    capacity = models.SmallIntegerField(null=False, default=0, verbose_name=_("ظرفیت"))
    extra_person = models.SmallIntegerField(null=True, blank=True, default=0, verbose_name=_("نفر اضافه"))
    default_cover = models.ForeignKey(Room_cover, on_delete=models.SET_NULL, null=True,
                                      verbose_name=_("عکس پس زمینه"))
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=1, verbose_name=_("فعال"))
    upd_add = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ آپدیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('تاریخ ایجاد'))

    def __str__(self):
        return str(self.title )

    class Meta:
        verbose_name_plural = _("اتاق ها")
        verbose_name = _("اتاق ها")

    def __unicode__(self):
        return _("اتاق ها")


class Room_images(models.Model):
    TYPE_TRUE = ((1, 'Yes'), (0, 'NO'),)

    def validate_image(self):
        filesize = self.file.size
        megabyte_limit = 1
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError(_("Max file size is %sMB") % str(megabyte_limit))

    file = models.ImageField(upload_to=file_room, null=False, default=None, validators=[validate_image],
                             help_text=_('Maximum file size allowed is 1Mb'), verbose_name=_("فایل"))
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("اتاق"))
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=1, verbose_name=_("فعال"))
    date_upd = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ آپدیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('تاریخ ایجاد'))

    def file_uploaded(self):
        ext = self.file.url.split('.')[-1].lower()
        valid_extensions = ['jpg', 'png', 'jpeg']
        if ext in valid_extensions:
            return format_html('<img style="width: 100px;" src="{}" />'.format(self.file.url))
        else:
            return format_html('<a href="{}">Click Me</a>'.format(self.file.url))

    class Meta:
        verbose_name_plural = _("تصاویر اتاق ها")
        verbose_name = _("تصاویر اتاق ها")

    def __str__(self):
        return str(self.pk)


class Room_facility(models.Model):
    TYPE_TRUE = ((1, 'Yes'), (0, 'NO'),)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(null=True, max_length=255, verbose_name=_("عنوان"))
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=1, verbose_name=_("فعال"))
    date_upd = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ آپدیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('تاریخ ایجاد'))

    class Meta:
        verbose_name_plural = _("امکانات اتاق ها")
        verbose_name = _("امکانات اتاق ها")

    def __str__(self):
        return str(self.title)


class Reviews(models.Model):
    TYPE_TRUE = ((1, 'نمایان'), (0, 'مخفی'),)
    TYPE_STARS = ((1, '1'), (2, '2'), (4, '3'), (4, '4'), (5, '5'),)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, verbose_name=_("نام هتل"))
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_("مشتری"))
    stars = models.SmallIntegerField(choices=TYPE_STARS, null=False, default=0, verbose_name=_("ستاره"))
    title = models.CharField(null=False, default=None, max_length=255, verbose_name=_("عنوان"))
    short_desc = models.TextField(null=True, blank=True, default=None, verbose_name=_("توضیحات کوتاه"))
    desc_good = models.TextField(null=True, blank=True, verbose_name=_("نکات مثبت"))
    desc_bad = models.TextField(null=True, blank=True, verbose_name=_("نکات منفی"))
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=0, verbose_name=_("وضعیت مشاهده"))
    date_upd = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ آپدیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('تاریخ ایجاد'))

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = _("دیدگاه ها")
        verbose_name = _("دیدگاه ها")

    def __str__(self):
        return str(self.title)


class Reviews_reply(models.Model):
    TYPE_TRUE = ((1, 'نمایان'), (0, 'مخفی'),)
    reviews = models.ForeignKey(Reviews, on_delete=models.SET_NULL, blank=True, null=True)
    short_desc = models.TextField(null=True, blank=True, default=None, verbose_name=_("توضیحات کوتاه"))
    date_upd = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ آپدیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('تاریخ ایجاد'))

    def __unicode__(self):
        return self.short_desc

    class Meta:
        verbose_name_plural = _("جواب دیدگاه ها")
        verbose_name = _("جواب دیدگاه ها")

    def __str__(self):
        return str(self.short_desc)


class Discount(models.Model):
    TYPE_TRUE = ((1, 'فعال'), (0, 'غیرفعال'),)
    TYPE_FLAG = ((1, 1), (0, 0),)
    TYPE_DISCOUNT = ((1, 'درصد'), (2, 'مقدار'),)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, blank=True, null=True, related_name="hotel_discount", verbose_name=_("هتل"))
    title = models.CharField(null=True, blank=True, max_length=255, verbose_name=_("عنوان تخفیف"))
    reduction_type = models.SmallIntegerField(choices=TYPE_DISCOUNT, null=False, default=1, verbose_name=_("نوع تخفیف"))
    reduction = models.DecimalField(null=True, max_digits=12, decimal_places=2, default=0, verbose_name=_("مقدار"))
    start_date = models.DateTimeField(null=False, default=0, verbose_name=_("تاریخ شروع"))
    end_date = models.DateTimeField(null=False, default=0, verbose_name=_("تاریخ پایان"))
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=0, verbose_name=_("فعال"))
    flag_pricing = models.SmallIntegerField(choices=TYPE_FLAG, null=False, default=0, verbose_name=_("قیمت گذاری"))
    date_upd = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ آپدیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('تاریخ ایجاد'))
    def save(self, *args, **kwargs):
        for i in Room.objects.filter(hotel_id=self.hotel_id).all():
            chk = Discount_room.objects.filter(room=i, discount_id=self.pk).first()
            if chk is None:
                check = Discount_room()
                check.room = i
                check.discount_id = self.pk
                check.reduction = self.reduction
                check.save()
        super(Discount, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = _("تخفیف ها")
        verbose_name = _("تخفیف ها")

    def __str__(self):
        return str(self.title)

class Discount_room(models.Model):
    TYPE_TRUE = ((1, 'Yes'), (0, 'NO'),)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name="discount_room", verbose_name=_("اتاق"))
    discount = models.ForeignKey("Discount", on_delete=models.SET_NULL, null=True, related_name="discount", verbose_name=_("تخفیف"))
    reduction = models.DecimalField(null=True, max_digits=12, decimal_places=2, default=0, verbose_name=_("مقدار"))
    date_upd = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ آپدیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('تاریخ ایجاد'))

    def __unicode__(self):
        return self.room

    class Meta:
        verbose_name_plural = _("تخفیف اتاق ها")
        verbose_name = _("تخفیف اتاق ها")

    def __str__(self):
        return str(self.room)

class Room_pricing(models.Model):
    TYPE_TRUE = ((1, 'Yes'), (0, 'NO'),)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name="room_pricing", verbose_name=_("اتاق"))
    calender_pricing = models.ForeignKey("Calender_pricing", on_delete=models.SET_NULL, null=True, related_name="calender_pricing", verbose_name=_("تاریخ"))
    board = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=2, default=0, verbose_name=_("قیمت برد"))
    price = models.DecimalField(null=True, max_digits=12, decimal_places=2, default=0, verbose_name=_("قیمت هتل تیک"))
    date_upd = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ آپدیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('تاریخ ایجاد'))

    class Meta:
        verbose_name_plural = _("قیمت گذاری ها")
        verbose_name = _("قیمت گذاری ها")


    def customer_price(self):
        discount = Discount.objects.filter(active=1, hotel_id=self.calender_pricing.hotel_id, start_date__lt=timezone.now(),
                                           end_date__gt=timezone.now()).first()
        if discount is not None:
            red = discount.reduction
            red_type = discount.reduction_type
            if red_type == 1:  # perc
                return self.board - self.board * (red / 100)
            else:
                return self.board - int(red)
        else:
            return self.board

    def __str__(self):
        return str(self.room)

    def save(self, *args, **kwargs):
        if self.calender_pricing is not None:
            reduction_type = self.calender_pricing.reduction_type
            reduction = self.calender_pricing.reduction
            if reduction_type == 1: #perc
                price = self.board * int(reduction) / 100
            else:
                price = self.board - int(reduction)
            self.price = round(price)
            super(Room_pricing, self).save(*args, **kwargs)

class Calender_pricing(models.Model):
    TYPE_REDUCTION = ((1, 'درصد'), (2, 'مقدار'),)
    TYPE_DISCOUNT = ((0, 'نیاز ندارم'),(1, 'درصد'), (2, 'مقدار'),)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, related_name="hotel_calender_pricing", verbose_name=_("هتل"))
    start_date = models.DateField(null=True, verbose_name=_('تاریخ شروع'))
    end_date = models.DateField(null=True, verbose_name=_('تاریخ پایان'))
    reduction_type = models.SmallIntegerField(choices=TYPE_REDUCTION, null=False, default=1, verbose_name=_("نوع قیمت"))
    reduction = models.DecimalField(null=True, max_digits=12, decimal_places=2, default=0, verbose_name=_("مقدار"))
    dis_reduction_type = models.SmallIntegerField(choices=TYPE_DISCOUNT, null=False, default=0, verbose_name=_("نوع تخفیف"))
    dis_reduction = models.DecimalField(null=True, max_digits=12, decimal_places=2, default=0, verbose_name=_("مقدار تخفیف"))
    date_upd = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ آپدیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('تاریخ ایجاد'))

    class Meta:
        verbose_name_plural = _("تقویم قیمت ها")
        verbose_name = _("تقویم قیمت ها")

    def __str__(self):
        return str(self.hotel)
    def save(self, *args, **kwargs):
        if self.dis_reduction_type != 0:
            check = Discount.objects.filter(hotel_id=self.hotel_id, flag_pricing=1)
            if check.first() is None:
                discount = Discount()
                discount.hotel = self.hotel
                discount.title = 'From Pricing'
                discount.reduction_type = self.dis_reduction_type
                discount.reduction = self.dis_reduction
                discount.start_date = self.start_date
                discount.end_date = self.end_date
                discount.active = 1
                discount.flag_pricing = 1
                discount.save()
            else:
                check = check.get()
                check.end_date = self.end_date
                check.start_date = self.start_date
                check.reduction = self.dis_reduction
                check.reduction_type = self.dis_reduction_type
                check.active = 1
                check.save()
        for i in Room_pricing.objects.filter(calender_pricing_id=self.pk).all():
            reduction_type = self.reduction_type
            reduction = self.reduction
            if reduction_type == 1:  # perc
                price = i.board * int(reduction) / 100
            else:
                price = i.board - int(reduction)
            Room_pricing.objects.filter(pk=i.pk).update(price=price)
        for i in Room.objects.filter(hotel_id=self.hotel_id).all():
            chk = Room_pricing.objects.filter(room=i, calender_pricing_id=self.pk).first()
            if chk is None:
                check = Room_pricing()
                check.room = i
                check.calender_pricing_id = self.pk
                check.board = 0
                check.save()
        super(Calender_pricing, self).save(*args, **kwargs)




class Calender_quantity(models.Model):
    TYPE_TRUE = ((1, _('جا دارد')), (0, _('جا ندارد')),)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, related_name="hotel_calender_quantity", verbose_name=_("هتل"))
    start_date = models.DateField(null=True, verbose_name=_('تاریخ شروع'))
    end_date = models.DateField(null=True, verbose_name=_('تاریخ پایان'))
    saturday = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=1, verbose_name=_("شنبه"))
    sunday = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=1, verbose_name=_("یکشنبه"))
    monday = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=1, verbose_name=_("دوشنبه"))
    tuesday = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=1, verbose_name=_("سه شنبه"))
    wednesday = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=1, verbose_name=_("چهارشنبه"))
    thursday = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=1, verbose_name=_("پنج شنبه"))
    friday = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=1, verbose_name=_("جمعه"))
    date_upd = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ آپدیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('تاریخ ایجاد'))
    class Meta:
        verbose_name_plural = _("تقویم ظرفیت ها")
        verbose_name = _("تقویم ظرفیت ها")

    def __str__(self):
        return str(_('ظرفیت ها'))


class Room_quantity(models.Model):
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name="room_quantity", verbose_name=_("اتاق"))
    calender_quantity = models.ForeignKey(Calender_quantity, on_delete=models.SET_NULL, null=True, related_name="calender_quantity", verbose_name=_("تاریخ"))
    date_upd = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ آپدیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('تاریخ ایجاد'))

    class Meta:
        verbose_name_plural = _("ظرفیت ها")
        verbose_name = _("ظرفیت ها")

    def __str__(self):
        return str(self.room)