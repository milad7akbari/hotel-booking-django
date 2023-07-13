import os

from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import models


def file_category(self, filename):
    ext = filename.split('.')[-1]
    if self.pk is None:
        pk = 1
    else:
        pk = self.pk + 1
    filename = "%s.%s" % (str(pk), ext)
    return os.path.join('media/blogs/files/', filename)


class Category(models.Model):
    TYPE_CHOICES = ((1, 'Yes'), (0, 'No'),)
    title = models.CharField(null=True, max_length=256)
    desc = models.TextField(null=True)
    flag = models.SmallIntegerField(default=0, choices=TYPE_CHOICES,
                                    help_text=_('اگر Yes باشد در هدر سایت در بخش بلاگ ها نمایش داده خواهد شد!'))
    active = models.SmallIntegerField(null=False, default=0)
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Category Blog"

    def __str__(self):
        return self.title


class Main(models.Model):
    category_blog = models.ForeignKey(Category, default=None, on_delete=models.CASCADE)
    default_image = models.ForeignKey('Files', null=True, on_delete=models.CASCADE)
    title = models.CharField(null=False, blank=False, default=0, max_length=256)
    desc = models.TextField(null=True)
    active = models.SmallIntegerField(null=False, default=0)
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Blog"

    def __str__(self):
        return self.title


class Files(models.Model):
    def validate_image(self):
        filesize = self.file.size
        megabyte_limit = 1
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError(_("Max file size is %sMB") % str(megabyte_limit))

    file = models.ImageField(upload_to=file_category, blank=True, null=True, validators=[validate_image],
                             help_text=_('Maximum file size allowed is 1Mb'))
    title = models.CharField(null=True, max_length=256)
    note = models.CharField(null=True, max_length=256)
    active = models.SmallIntegerField(null=False, default=0)
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
        verbose_name = "Blog File"

    def __str__(self):
        return self.note
