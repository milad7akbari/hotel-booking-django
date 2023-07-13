import os
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    USER_TYPE_CHOICES = ((1, 'admin'), (2, 'customer'),)
    national_code = models.CharField(null=True, max_length=128)
    birthday = models.DateField(blank=True, null=True)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=2)

    def __unicode__(self):
        return self.username

    def save(self, *args, **kwargs):
        password = make_password(self.password, salt="Argon2PasswordHasher", hasher="default")
        self.password = password
        if len(self.username) == 10:
            username = '09' + self.username[1:]
        else:
            username = self.username
        self.username = username
        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "User"

    def __str__(self):
        return self.username


def file_category(self, filename):
    ext = filename.split('.')[-1]
    if self.pk is None:
        pk = 1
    else:
        pk = self.pk + 1
    filename = "%s.%s" % (str(pk), ext)
    return os.path.join('media/slider/images/', filename)


class Slider(models.Model):
    def validate_image(self):
        filesize = self.file.size
        megabyte_limit = 10.5
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError(_("Max file size is %sMB") % str(megabyte_limit))

    file = models.ImageField(upload_to=file_category, blank=True, null=True, validators=[validate_image],
                             help_text=_('Maximum file size allowed is 1Mb'))
    title = models.CharField(max_length=255)
    active = models.SmallIntegerField(null=False, default=0)
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    def img_preview(self):
        return format_html('<img style="width: 100px;" src="{}" />'.format(self.file.url))

    class Meta:
        verbose_name = "Slider"

    def __str__(self):
        return self.title


class Forgot_password(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0, null=True)
    token = models.CharField(max_length=255, default=0, null=True)
    status = models.SmallIntegerField(null=False, default=0)
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Forgot Password Users"

    def __str__(self):
        return self.user.first_name

    def __unicode__(self):
        return self.user.first_name


class Provinces(models.Model):
    name = models.CharField(null=True, max_length=128)
    latitude = models.DecimalField(null=True, max_digits=10, decimal_places=8)
    longitude = models.DecimalField(null=True, max_digits=11, decimal_places=8)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Provinces"
        verbose_name_plural = "Provinces"


    def __str__(self):
        return self.name

class Cities(models.Model):
    provinces = models.ForeignKey(Provinces, default=None, on_delete=models.CASCADE)
    name = models.CharField(null=True, max_length=128)
    latitude = models.DecimalField(null=True, max_digits=10, decimal_places=8)
    longitude = models.DecimalField(null=True, max_digits=11, decimal_places=8)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = "Cities"
        verbose_name_plural = "Cities"


    def __str__(self):
        return self.name

class Meta(models.Model):
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    keywords = models.TextField(blank=True, help_text="some tag, hoteltik, international, etc...")
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return 'Meta'

    class Meta:
        verbose_name_plural = "Meta"
        verbose_name = "Meta"

    def __unicode__(self):
        return 'Meta'
