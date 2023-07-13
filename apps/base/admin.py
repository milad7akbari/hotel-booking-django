from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Slider, Meta


class SliderAdmin(TranslationAdmin):
    model = Slider
    list_display = ('pk', 'file', 'title', 'active', 'date_add')

class MetaAdmin(TranslationAdmin):
    model = Meta
    list_display = ('title', 'description', 'keywords')

# class HotelAdmin(TranslationAdmin):
#     model = Hotel
#     list_display = ('name', 'reference', 'stars', 'on_sale', 'active', 'date_add')
#     readonly_fields = ('reference',)

# class ImagesAdmin(TranslationAdmin):
#     model = Images
#     list_display = ('pk', 'file', 'title', 'active', 'date_add')

admin.site.register(Slider, SliderAdmin)
admin.site.register(Meta, MetaAdmin)
