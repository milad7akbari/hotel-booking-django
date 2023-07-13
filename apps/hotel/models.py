import datetime
import os

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum, F, Q
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from pyexpat.errors import messages

from apps.base.models import Cities, User


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
    name = models.CharField(null=True, max_length=256)
    reference = models.CharField(null=True, max_length=256, unique=True)
    long_desc = models.TextField(null=True)
    short_desc = models.TextField(null=True, blank=True)
    rule_cancelable = models.TextField(null=True, blank=True)
    rule_enter = models.TextField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    city = models.ForeignKey(Cities, null=True, on_delete=models.CASCADE)
    address = models.TextField(null=True)
    latitude = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    longitude = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    phone_number = models.CharField(null=True, max_length=256)
    number_rooms = models.SmallIntegerField(null=False, default=0)
    number_floor = models.SmallIntegerField(null=False, default=0)
    stars = models.PositiveSmallIntegerField(choices=TYPE_STARS, default=1)
    default_cover = models.ForeignKey('Cover', null=True, on_delete=models.CASCADE)
    meta_keywords = models.CharField(default=None, blank=True, max_length=256,
                                     help_text="some tag, espinas, international, etc...")
    available_for_order = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=1)
    has_early_check_in_out = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=1)
    has_breakfast = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=1)
    on_sale = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=0)
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=0)
    upd_add = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Hotel "
        verbose_name = "Hotel"

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
    hotel = models.ForeignKey(Hotel, null=True, on_delete=models.CASCADE)
    title = models.CharField(null=True, max_length=256)
    note = models.CharField(null=True, blank=True, max_length=256)
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=0)
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
        verbose_name_plural = "Hotel Images"
        verbose_name = "Hotel Images"

    def __str__(self):
        return self.note


class Cover(models.Model):
    TYPE_TRUE = ((1, 'Yes'), (0, 'NO'),)

    def validate_image(self):
        filesize = self.file.size
        megabyte_limit = 1
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError(_("Max file size is %sMB") % str(megabyte_limit))

    file = models.ImageField(upload_to=file, blank=True, null=True, validators=[validate_image],
                             help_text=_('Maximum file size allowed is 1Mb'))
    title = models.CharField(null=True, max_length=256)
    note = models.CharField(null=True, blank=True, max_length=256)
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=0)
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
        verbose_name_plural = "Hotel Cover"
        verbose_name = "Hotel Cover"

    def __str__(self):
        return self.note


class Facility(models.Model):
    TYPE_TRUE = ((1, 'Yes'), (0, 'NO'),)
    hotel = models.ForeignKey(Hotel, null=True, on_delete=models.CASCADE)
    title = models.CharField(null=True, max_length=256)
    note = models.CharField(null=False, blank=True, default=None, max_length=256)
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=0)
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = "Hotel Facility"
        verbose_name = "Hotel Facility"

    def __str__(self):
        return self.title


class Extra_person_rate(models.Model):
    TYPE_TRUE = ((1, 'Yes'), (0, 'NO'),)
    hotel = models.OneToOneField(Hotel, null=True, on_delete=models.CASCADE)
    rate = models.DecimalField(null=True, max_digits=9, decimal_places=2)
    note = models.CharField(null=False, default=None, max_length=256)
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=1)
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = "Extra Person Rate"
        verbose_name = "Extra Person Rate"

    def __str__(self):
        return self.hotel.name


class Breakfast_rate(models.Model):
    TYPE_TRUE = ((1, 'Yes'), (0, 'NO'),)
    hotel = models.OneToOneField(Hotel, null=True, on_delete=models.CASCADE)
    rate = models.DecimalField(null=True, max_digits=9, decimal_places=2)
    note = models.CharField(null=False, default=None, max_length=256)
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=1)
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = "Breakfast Rate"
        verbose_name = "Breakfast Rate"

    def __str__(self):
        return self.hotel.name


class Check_in_out_rate(models.Model):
    TYPE_TRUE = ((1, 'Yes'), (0, 'NO'),)
    hotel = models.OneToOneField(Hotel, null=True, on_delete=models.CASCADE)
    rate = models.DecimalField(null=True, max_digits=9, decimal_places=2)
    note = models.CharField(null=False, default=None, max_length=256)
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=1)
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = "Check In Out Rate"
        verbose_name = "Check In Out Rate"

    def __str__(self):
        return self.hotel.name


class Close_spots(models.Model):
    TYPE_TRUE = ((1, 'Yes'), (0, 'NO'),)
    hotel = models.ForeignKey(Hotel, null=True, on_delete=models.CASCADE)
    short_desc = models.CharField(null=True, max_length=512)
    note = models.CharField(default=None, blank=True, max_length=512)
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=0)
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = "Hotel Close Spots"
        verbose_name = "Hotel Close Spots"

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
    title = models.CharField(null=True, max_length=256)
    note = models.CharField(null=True, blank=True, max_length=256)
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=1)
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
        verbose_name_plural = "Room Cover"
        verbose_name = "Room Cover"

    def __str__(self):
        return self.title


class Room(models.Model):
    TYPE_TRUE = ((1, 'Yes'), (0, 'NO'),)
    title = models.CharField(null=True, max_length=256)
    hotel = models.ForeignKey(Hotel, null=True, on_delete=models.CASCADE)
    price = models.DecimalField(null=True, max_digits=9, decimal_places=2)
    short_desc = models.TextField(null=True)
    note = models.TextField(null=True)
    number_floor = models.SmallIntegerField(null=False, default=0)
    count = models.SmallIntegerField(null=False, default=0)
    capacity = models.SmallIntegerField(null=False, default=0)
    extra_person = models.SmallIntegerField(null=False, default=0)
    default_cover = models.OneToOneField(Room_cover, null=True, on_delete=models.CASCADE)
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=0)
    upd_add = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Room"
        verbose_name = "Room"

    def __unicode__(self):
        return 'Room'


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
    title = models.CharField(null=True, max_length=256)
    note = models.CharField(null=True, blank=True, max_length=256)
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=0)
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
        verbose_name_plural = "Room Images"
        verbose_name = "Room Images"

    def __str__(self):
        return self.title


class Room_facility(models.Model):
    TYPE_TRUE = ((1, 'Yes'), (0, 'NO'),)
    room = models.ForeignKey(Room, null=True, on_delete=models.CASCADE)
    title = models.CharField(null=True, max_length=256)
    note = models.CharField(null=False, blank=True, default=None, max_length=256)
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=0)
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = "Room Facility"
        verbose_name = "Room Facility"

    def __str__(self):
        return self.title


class Reviews(models.Model):
    TYPE_TRUE = ((1, 'نمایان'), (0, 'مخفی'),)
    TYPE_STARS = ((1, '1'), (2, '2'), (4, '3'), (4, '4'), (5, '5'),)
    hotel = models.ForeignKey(Hotel, default=None, on_delete=models.CASCADE)
    user = models.ForeignKey(User,null=True, blank=True, default=None, on_delete=models.CASCADE)
    stars = models.SmallIntegerField(choices=TYPE_STARS, null=False, default=0)
    title = models.CharField(null=False, default=None, max_length=256)
    short_desc = models.TextField(null=True, blank=True, default=None, )
    desc_good = models.TextField(null=True, blank=True)
    desc_bad = models.TextField(null=True, blank=True)
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=0)
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Hotel Reviews"
        verbose_name = "Hotel Reviews"

    def __str__(self):
        return self.title

class Reviews_reply(models.Model):
    TYPE_TRUE = ((1, 'نمایان'), (0, 'مخفی'),)
    reviews = models.ForeignKey(Reviews, default=None, on_delete=models.CASCADE)
    short_desc = models.TextField(null=True, blank=True, default=None, )
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=0)
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return self.short_desc

    class Meta:
        verbose_name_plural = "Hotel Reviews Reply"
        verbose_name = "Hotel Reviews Reply"

    def __str__(self):
        return self.short_desc


class Discount(models.Model):
    TYPE_TRUE = ((1, 'فعال'), (0, 'غیرفعال'),)
    TYPE_DISCOUNT = ((1, 'درصد'), (2, 'مقدار'),)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, default=0, null=True, related_name="room_discount")
    title = models.CharField(null=True, max_length=256)
    reduction_type = models.SmallIntegerField(choices=TYPE_DISCOUNT,null=False, default=1)
    reduction = models.DecimalField(null=True, max_digits=9, decimal_places=2)
    start_date = models.DateTimeField(null=False, default=0)
    end_date = models.DateTimeField(null=False, default=0)
    active = models.SmallIntegerField(choices=TYPE_TRUE, null=False, default=0)
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
        verbose_name_plural = "Hotel Discount"
        verbose_name = "Hotel Discount"

    def __str__(self):
        return self.title
