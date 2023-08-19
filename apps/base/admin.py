from django.contrib import admin
from django.db import models
from django.forms import Textarea
from modeltranslation.admin import TranslationAdmin
from .models import Slider, Meta, Provinces, Cities, Footer, Pages, Configuration


class FooterAdmin(admin.ModelAdmin):
    model = Footer
    list_display = ('name','value','date_upd','date_add')

class SliderAdmin(admin.ModelAdmin):
    model = Slider
    list_filter = ('active',)
    list_display = ('pk', 'file', 'active', 'date_add')

class MetaAdmin(TranslationAdmin):
    model = Meta
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 80, })},
    }
    list_filter = ('page_name',)
    list_display = ('page_name', 'title', 'description', 'keywords')

class PagesAdmin(TranslationAdmin):
    model = Pages
    list_filter = ('page_name',)
    list_display = ('page_name', 'description')

from django_summernote.utils import get_attachment_model

class ConfigurationAdmin(admin.ModelAdmin):
    model = Configuration
    list_display = ('name', 'value', 'date_add')


class ProvincesAdmin(TranslationAdmin):
    model = Provinces
    list_display = ('name','latitude','longitude','created_at',)

class CitiesAdmin(TranslationAdmin):
    model = Cities
    list_select_related = ('provinces', )
    list_display = ( 'name', 'provinces','file', 'latitude', 'longitude','created_at')


# class HotelAdmin(TranslationAdmin):
#     model = Hotel
#     list_display = ('name', 'reference', 'stars', 'on_sale', 'active', 'date_add')
#     readonly_fields = ('reference',)

# class ImagesAdmin(TranslationAdmin):
#     model = Images
#     list_display = ('pk', 'file', 'title', 'active', 'date_add')

admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(Pages, PagesAdmin)
admin.site.register(Footer, FooterAdmin)
admin.site.unregister(get_attachment_model())
admin.site.register(Provinces, ProvincesAdmin)
admin.site.register(Cities, CitiesAdmin)
admin.site.register(Slider, SliderAdmin)
admin.site.register(Meta, MetaAdmin)
