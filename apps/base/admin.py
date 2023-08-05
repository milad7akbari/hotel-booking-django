from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Slider, Meta, Provinces, Cities, Footer, Pages


class FooterAdmin(admin.ModelAdmin):
    model = Footer
    list_display = ('name','value','date_upd','date_add')

class SliderAdmin(TranslationAdmin):
    model = Slider
    list_display = ('pk', 'file', 'title', 'active', 'date_add')

class MetaAdmin(TranslationAdmin):
    model = Meta
    list_display = ('page_name', 'title', 'description', 'keywords')

class PagesAdmin(TranslationAdmin):
    model = Pages
    list_display = ('page_name', 'description')


class ProvincesAdmin(TranslationAdmin):
    model = Provinces
    list_display = ('name',)

class CitiesAdmin(TranslationAdmin):
    model = Cities
    list_display = ('name',)


# class HotelAdmin(TranslationAdmin):
#     model = Hotel
#     list_display = ('name', 'reference', 'stars', 'on_sale', 'active', 'date_add')
#     readonly_fields = ('reference',)

# class ImagesAdmin(TranslationAdmin):
#     model = Images
#     list_display = ('pk', 'file', 'title', 'active', 'date_add')

admin.site.register(Pages, PagesAdmin)
admin.site.register(Footer, FooterAdmin)
admin.site.register(Provinces, ProvincesAdmin)
admin.site.register(Cities, CitiesAdmin)
admin.site.register(Slider, SliderAdmin)
admin.site.register(Meta, MetaAdmin)
