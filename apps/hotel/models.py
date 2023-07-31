import os

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

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
    name = models.CharField(null=True, max_length=255, verbose_name=_("نام هتل"))
    reference = models.CharField(null=True, max_length=255, unique=True, verbose_name=_("رفرنس"))
    long_desc = models.TextField(null=True, verbose_name=_("توضیحات بلند"))
    short_desc = models.TextField(null=True, blank=True, verbose_name=_("توضیحات کوتاه"))
    rule_cancelable = models.TextField(null=True, blank=True, verbose_name=_("قوانین کنسل"))
    rule_enter = models.TextField(null=True, blank=True, verbose_name=_("قوانین ورود و خروج"))
    note = models.TextField(null=True, blank=True, verbose_name=_("نوت"))
    city = models.ForeignKey(Cities, null=True, on_delete=models.CASCADE, verbose_name=_("شهر"))
    address = models.TextField(null=True, verbose_name=_("آدرس"))
    latitude = models.DecimalField(null=True, max_digits=12, decimal_places=8)
    longitude = models.DecimalField(null=True, max_digits=12, decimal_places=8)
    phone_number = models.CharField(null=True, max_length=255, verbose_name=_("شماره تلفن"))
    number_rooms = models.SmallIntegerField(null=False, default=0, verbose_name=_("تعداد اتاق ها"))
    number_floor = models.SmallIntegerField(null=False, default=0, verbose_name=_("تعداد طبقه"))
    stars = models.PositiveSmallIntegerField(choices=TYPE_STARS, default=1, verbose_name=_("ستاره ها"))
    default_cover = models.ForeignKey('Cover', null=True, on_delete=models.CASCADE, verbose_name=_("عکس پیش فرض"))
    meta_keywords = models.CharField(default=None, blank=True, max_length=255,
                                     help_text="some tag, espinas, international, etc...", verbose_name=_("متا کیبورد"))
    has_early_check_in_out = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=1, verbose_name=_("دارای ورود و خروج زود هنگام"))
    has_breakfast = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=1, verbose_name=_("دارای صبحانه"))
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=0, verbose_name=_("فعال"))
    upd_add = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

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
    hotel = models.ForeignKey(Hotel, null=True, on_delete=models.CASCADE, verbose_name=_("نام هتل"))
    title = models.CharField(null=True, max_length=255, verbose_name=_("عنوان"))
    note = models.CharField(null=True, blank=True, max_length=255, verbose_name=_("نوت"))
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=0, verbose_name=_("فعال"))
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

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
        return self.title


class Cover(models.Model):
    TYPE_TRUE = ((1, 'Yes'), (0, 'NO'),)

    def validate_image(self):
        filesize = self.file.size
        megabyte_limit = 1
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError(_("Max file size is %sMB") % str(megabyte_limit))

    file = models.ImageField(upload_to=file, blank=True, null=True, validators=[validate_image],
                             help_text=_('Maximum file size allowed is 1Mb'))
    title = models.CharField(null=True, max_length=255, verbose_name=_("عنوان"))
    note = models.CharField(null=True, blank=True, max_length=255, verbose_name=_("نوت"))
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=0, verbose_name=_("فعال"))
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

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
        return self.title


class Facility(models.Model):
    TYPE_TRUE = ((1, 'Yes'), (0, 'NO'),)
    hotel = models.ForeignKey(Hotel, null=True, on_delete=models.CASCADE, verbose_name=_("نام هتل"))
    title = models.CharField(null=True, max_length=255, verbose_name=_("عنوان"))
    note = models.CharField(null=False, blank=True, default=None, max_length=255, verbose_name=_("نوت"))
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=0, verbose_name=_("فعال"))
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural =  _("امکانات  هتل ها")
        verbose_name =  _("امکانات  هتل ها")

    def __str__(self):
        return self.title


class Extra_person_rate(models.Model):
    TYPE_TRUE = ((1, 'Yes'), (0, 'NO'),)
    hotel = models.OneToOneField(Hotel, null=True, on_delete=models.CASCADE, related_name='extra_person_rate', verbose_name=_("نام هتل"))
    rate = models.DecimalField(null=True, max_digits=12, decimal_places=2, default=0, verbose_name=_("قیمت"))
    note = models.CharField(null=False, default=None, max_length=255, verbose_name=_("نوت"))
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=1, verbose_name=_("فعال"))
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = _("نفر اضافه")
        verbose_name = _("نفر اضافه")

    def __str__(self):
        return self.hotel.name


class Breakfast_rate(models.Model):
    TYPE_TRUE = ((1, 'Yes'), (0, 'NO'),)
    hotel = models.OneToOneField(Hotel, null=True, on_delete=models.CASCADE, related_name='breakfast_rate', verbose_name=_("نام هتل"))
    rate = models.DecimalField(null=True, max_digits=12, decimal_places=2, default=0, verbose_name=_("قیمت"))
    note = models.CharField(null=False, default=None, max_length=255, verbose_name=_("نوت"))
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=1, verbose_name=_("فعال"))
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = _("نرخ صبحانه")
        verbose_name = _("نرخ صبحانه")

    def __str__(self):
        return self.hotel.name


class Check_in_out_rate(models.Model):
    TYPE_TRUE = ((1, 'Yes'), (0, 'NO'),)
    hotel = models.OneToOneField(Hotel, null=True, on_delete=models.CASCADE, related_name='check_in_out_rate', verbose_name=_("نام هتل"))
    rate = models.DecimalField(null=True, max_digits=12, decimal_places=2, default=0, verbose_name=_("قیمت"))
    note = models.CharField(null=False, default=None, max_length=255, verbose_name=_("نوت"))
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=1, verbose_name=_("فعال"))
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = _("نرخ ورود و خروج")
        verbose_name = _("نرخ ورود و خروج")

    def __str__(self):
        return self.hotel.name


class Close_spots(models.Model):
    TYPE_TRUE = ((1, 'Yes'), (0, 'NO'),)
    hotel = models.ForeignKey(Hotel, null=True, on_delete=models.CASCADE, verbose_name=_("نام هتل"))
    short_desc = models.CharField(null=True, max_length=512, verbose_name=_("توضیحات کوتاه"))
    note = models.CharField(default=None, blank=True, max_length=512, verbose_name=_("نوت"))
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=0, verbose_name=_("فعال"))
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = _("مکان های نزدیک")
        verbose_name = _("مکان های نزدیک")

    def __str__(self):
        return self.short_desc


class Room_cover(models.Model):
    TYPE_TRUE = ((1, 'Yes'), (0, 'NO'),)

    def validate_image(self):
        filesize = self.file.size
        megabyte_limit = 1
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError(_("Max file size is %sMB") % str(megabyte_limit))

    file = models.ImageField(upload_to=file_room, blank=True, null=True, validators=[validate_image],
                             help_text=_('Maximum file size allowed is 1Mb'))
    title = models.CharField(null=True, max_length=255, verbose_name=_("عنوان"))
    note = models.CharField(null=True, blank=True, max_length=255, verbose_name=_("نوت"))
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=1, verbose_name=_("فعال"))
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

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
        return self.title


class Room(models.Model):
    TYPE_TRUE = ((1, 'Yes'), (0, 'NO'),)
    title = models.CharField(null=True, max_length=255, verbose_name=_("عنوان"))
    hotel = models.ForeignKey(Hotel, null=True, on_delete=models.CASCADE, verbose_name=_("نام هتل"))
    base_price = models.DecimalField(null=True, max_digits=12, decimal_places=2, default=0, verbose_name=_("قیمت پابه"))
    price = models.DecimalField(null=True, max_digits=12, decimal_places=2, default=0, verbose_name=_("قیمت"))
    short_desc = models.TextField(null=True, verbose_name=_("توضیحات کوتاه"))
    note = models.TextField(null=True, verbose_name=_("نوت"))
    number_floor = models.SmallIntegerField(null=False, default=0, verbose_name=_("طبقه اتاق"))
    count = models.SmallIntegerField(null=False, default=0, verbose_name=_("تعداد اتاق"))
    capacity = models.SmallIntegerField(null=False, default=0, verbose_name=_("ظرفیت"))
    extra_person = models.SmallIntegerField(null=False, default=0, verbose_name=_("نفر اضافه"))
    default_cover = models.OneToOneField(Room_cover, null=True, on_delete=models.CASCADE, verbose_name=_("عکس پس زمینه"))
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=0, verbose_name=_("فعال"))
    upd_add = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural =_("اتاق ها")
        verbose_name =_("اتاق ها")

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
                             help_text=_('Maximum file size allowed is 1Mb'))
    room = models.ForeignKey(Room, null=True, on_delete=models.CASCADE)
    title = models.CharField(null=True, max_length=255, verbose_name=_("عنوان"))
    note = models.CharField(null=True, blank=True, max_length=255, verbose_name=_("نوت"))
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=0, verbose_name=_("فعال"))
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

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
        return self.title


class Room_facility(models.Model):
    TYPE_TRUE = ((1, 'Yes'), (0, 'NO'),)
    room = models.ForeignKey(Room, null=True, on_delete=models.CASCADE)
    title = models.CharField(null=True, max_length=255, verbose_name=_("عنوان"))
    note = models.CharField(null=False, blank=True, default=None, max_length=255, verbose_name=_("نوت"))
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=0, verbose_name=_("فعال"))
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = _("امکانات اتاق ها")
        verbose_name = _("امکانات اتاق ها")

    def __str__(self):
        return self.title


class Reviews(models.Model):
    TYPE_TRUE = ((1, 'نمایان'), (0, 'مخفی'),)
    TYPE_STARS = ((1, '1'), (2, '2'), (4, '3'), (4, '4'), (5, '5'),)
    hotel = models.ForeignKey(Hotel, default=None, on_delete=models.CASCADE, verbose_name=_("نام هتل"))
    user = models.ForeignKey(User,null=True, blank=True, default=None, on_delete=models.CASCADE)
    stars = models.SmallIntegerField(choices=TYPE_STARS, null=False, default=0)
    title = models.CharField(null=False, default=None, max_length=255, verbose_name=_("عنوان"))
    short_desc = models.TextField(null=True, blank=True, default=None, verbose_name=_("توضیحات کوتاه"))
    desc_good = models.TextField(null=True, blank=True, verbose_name=_("نکات مثبت"))
    desc_bad = models.TextField(null=True, blank=True, verbose_name=_("نکات منفی"))
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=0, verbose_name=_("فعال"))
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = _("دیدگاه ها")
        verbose_name = _("دیدگاه ها")

    def __str__(self):
        return self.title

class Reviews_reply(models.Model):
    TYPE_TRUE = ((1, 'نمایان'), (0, 'مخفی'),)
    reviews = models.ForeignKey(Reviews, default=None, on_delete=models.CASCADE)
    short_desc = models.TextField(null=True, blank=True, default=None, verbose_name=_("توضیحات کوتاه"))
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=0, verbose_name=_("وضعبت"))
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return self.short_desc

    class Meta:
        verbose_name_plural = _("جواب دیدگاه ها")
        verbose_name = _("جواب دیدگاه ها")

    def __str__(self):
        return self.short_desc


class Discount(models.Model):
    TYPE_TRUE = ((1, 'فعال'), (0, 'غیرفعال'),)
    TYPE_DISCOUNT = ((1, 'درصد'), (2, 'مقدار'),)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, related_name="hotel_discount")
    title = models.CharField(null=True, max_length=255, verbose_name=_("عنوان تخفیف"))
    reduction_type = models.SmallIntegerField(choices=TYPE_DISCOUNT,null=False, default=1, verbose_name=_("نوع تخفیف"))
    reduction = models.DecimalField(null=True, max_digits=12, decimal_places=2, default=0, verbose_name=_("مقدار"))
    start_date = models.DateTimeField(null=False, default=0, verbose_name=_("تاریخ شروع"))
    end_date = models.DateTimeField(null=False, default=0, verbose_name=_("تاریخ پایان"))
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=0, verbose_name=_("فعال"))
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)
    #
    # def clean(self):
    #     if self.end_date < datetime.datetime.now():
    #         raise ValidationError(_('تاریخ پایان باید بزرگتر از حال باشد'))
    #     if self.start_date > self.end_date:
    #         raise ValidationError(_('تاریخ پایان باید بزرگتر از شروع باشد'))
    #     count = Discount.objects.filter(Q(room_id=self.room))
    #
    #
    #     check = Discount.objects.filter(Q(active=True) & Q(room_id=self.room) &
    #         (Q(start_date__lte=self.start_date) & Q(start_date__lte=self.end_date)) |
    #         (Q(end_date__gte=self.end_date) & Q(end_date__gte=self.start_date))
    #        )
    #     if check.exists():
    #         raise ValidationError(_('برای این هتل تخفیف وجود دارد'))
    #     super(Discount, self).clean()

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = _("تخفیف ها")
        verbose_name = _("تخفیف ها")

    def __str__(self):
        return self.title
