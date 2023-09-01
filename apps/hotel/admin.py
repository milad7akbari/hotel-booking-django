from django.contrib import admin
from django.forms import Textarea
from django.utils import timezone
from jalali_date import datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline, TranslationStackedInline
from django.db import models
from django.forms import Textarea
from apps.hotel.models import Cover, Hotel, Facility, Close_spots, Images, Check_in_out_rate, \
    Extra_person_rate, Room_cover, Room_facility, Room_images, Room, Reviews, Discount, Room_pricing, Calender_quantity, \
    Room_quantity, Calender_pricing, Discount_room
from django.utils.translation import gettext_lazy as _


class ImagesInline(admin.TabularInline):
    model = Images
    extra = 1
    show_change_link = True


class Check_in_out_rateInline(admin.StackedInline):
    model = Check_in_out_rate
    extra = 1
    show_change_link = True


class Extra_person_rateInline(admin.StackedInline):
    model = Extra_person_rate
    extra = 1
    show_change_link = True


class RoomInline(TranslationTabularInline):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 80, })},
    }

    model = Room
    extra = 0
    list_display = ('title', 'capacity', 'extra_person', 'active')
    show_change_link = True


class CoverAdmin(admin.ModelAdmin):
    model = Cover
    list_display = ('pk', 'file', 'date_add')
    def has_module_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class HotelAdmin(TranslationAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 30, })},
    }


    search_fields = ['name']
    model = Hotel
    list_filter = ('active', 'stars')
    list_display = ('name', 'reference', 'stars', 'type', 'active', 'date_add')
    readonly_fields = ('reference',)
    inlines = [RoomInline, ImagesInline, Check_in_out_rateInline, Extra_person_rateInline]


class Room_imagesInline(admin.TabularInline):
    model = Room_images
    extra = 0
    list_select_related = ('room',)
    search_fields = ['room__title', ]
    list_display = ('room', 'date_add')

    def room(self, obj):
        return obj.room.title

    room.short_description = _('اتاق')


class Room_facilityInline(TranslationTabularInline):
    model = Room_facility
    extra = 0
    list_display = ('hotel', 'title', 'active', 'date_add')


class RoomAdmin(TranslationAdmin):
    model = Room
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 30, })},
    }
    autocomplete_fields = ('hotel',)

    search_fields = ['title', 'hotel__name']
    list_filter = ('active', 'capacity', 'capacity')
    list_select_related = ('hotel',)
    inlines = [Room_facilityInline, Room_imagesInline]
    list_display = ('title', 'hotel', 'capacity', 'extra_person', 'active')
    def get_form(self, request, obj=None, **kwargs):
        form = super(RoomAdmin, self).get_form(request, obj, **kwargs)
        field = form.base_fields["hotel"]
        field.widget.can_add_related = False
        field.widget.can_change_related = False
        field.widget.can_delete_related = False
        return form


class FacilityAdmin(TranslationAdmin):
    model = Facility
    list_select_related = ('hotel',)
    search_fields = ['hotel__name', 'title']
    list_filter = ('active',)
    list_display = ('hotel', 'title', 'active', 'date_add')


class Close_spotsAdmin(TranslationAdmin):
    model = Close_spots
    list_display = ('hotel', 'short_desc', 'active', 'date_add')
    list_select_related = ('hotel',)
    search_fields = ['hotel__name', 'short_desc']
    list_filter = ('active',)

    def hotel(self, obj):
        return obj.hotel.name

    hotel.short_description = _('هتل')


class ImagesAdmin(admin.ModelAdmin):
    model = Images
    list_display = ('hotel', 'file', 'date_add')
    list_select_related = ('hotel',)
    search_fields = ['hotel__name', ]

    def hotel(self, obj):
        return obj.hotel.name

    hotel.short_description = _('هتل')


class Room_pricingInline(admin.TabularInline):
    model = Room_pricing
    fields = ['room', 'board', 'customer_price', 'price', ]
    readonly_fields = ('price', 'customer_price','room',)
    extra = 0
    max_num = 0
    list_select_related = True
    def customer_price(self, obj):
        return obj.customer_price()
    customer_price.short_description = 'قیمت مشتری'
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        id = request.resolver_match.kwargs.get('object_id')
        room_pricing = Calender_pricing.objects.filter(pk=id).first()
        if room_pricing is not None:
            kwargs["queryset"] = Room.objects.filter(hotel=room_pricing.hotel)
        return super(Room_pricingInline, self).formfield_for_foreignkey(db_field, request, **kwargs)



class Calender_pricingAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    model = Calender_pricing
    list_select_related = ('hotel',)
    list_display = ('pk','start_date_', 'end_date_', 'reduction_type', 'reduction', 'dis_reduction_type', 'dis_reduction', 'hotel')
    search_fields = ['start_date', ]
    readonly_fields = ['dis_reduction_type', 'dis_reduction', ]
    inlines = [Room_pricingInline, ]
    autocomplete_fields = ('hotel',)

    @admin.display(description='تاریخ شروع', ordering='start_date')
    def start_date_(self, obj):
        return datetime2jalali(obj.start_date).strftime('%Y-%m-%d')

    @admin.display(description='تاریخ پایان', ordering='end_date')
    def end_date_(self, obj):
        return datetime2jalali(obj.end_date).strftime('%Y-%m-%d')

class Room_quantityInline(admin.StackedInline):
    model = Room_quantity
    extra = 0

    list_select_related = ('hotel', 'room', 'calender_quantity',)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        id = request.resolver_match.kwargs.get('object_id')
        room_quantity = Calender_quantity.objects.filter(pk=id).first()
        if room_quantity is not None:
            kwargs["queryset"] = Room.objects.filter(hotel=room_quantity.hotel)
        return super(Room_quantityInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

class Calender_quantityAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    model = Calender_quantity
    list_select_related = ('hotel',)
    autocomplete_fields = ('hotel',)

    list_display = ('pk', 'hotel_', 'start_date_', 'end_date_', 'saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday')
    inlines = [Room_quantityInline, ]
    @admin.display(description='هتل', ordering='hotel')
    def hotel_(self, obj):
        return obj.hotel

    @admin.display(description='تاریخ شروع', ordering='start_date')
    def start_date_(self, obj):
        return datetime2jalali(obj.start_date).strftime('%Y-%m-%d')
    @admin.display(description='تاریخ پایان', ordering='end_date')
    def end_date_(self, obj):
        return datetime2jalali(obj.end_date).strftime('%Y-%m-%d')
class Room_coverAdmin(admin.ModelAdmin):
    model = Room_cover
    list_display = ('date_add',)
    list_select_related = ('room',)
    search_fields = ['room__title', ]

    def has_module_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def room(self, obj):
        return obj.room.title

    room.short_description = _('اتاق')



class ReviewsAdmin(admin.ModelAdmin):
    model = Reviews
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 30, })},
    }
    list_display = ('hotel', 'user', 'stars', 'title', 'active', 'j_date_add')
    list_select_related = ('hotel', 'user',)
    search_fields = ['hotel__name', 'title']
    list_filter = ('active', 'stars',)
    autocomplete_fields = ('hotel',)

    def get_form(self, request, obj=None, **kwargs):
        form = super(ReviewsAdmin, self).get_form(request, obj, **kwargs)
        field = form.base_fields["hotel"]
        field.widget.can_add_related = False
        field.widget.can_change_related = False
        field.widget.can_delete_related = False
        return form
    def hotel(self, obj):
        return obj.hotel.name

    hotel.short_description = _('هتل')

    def user(self, obj):
        return obj.user.name

    user.short_description = _('مشتری')

    def j_date_add(self, obj):
        return datetime2jalali(obj.date_add).strftime('%Y-%m-%d')

    j_date_add.short_description = _('تاریخ ایجاد')


class Room_facilityAdmin(TranslationAdmin):
    model = Room_facility
    list_display = ('room_', 'title', 'active', 'j_date_add',)
    list_select_related = ('room',)
    search_fields = ['room__title', 'title']
    list_filter = ('active',)

    def room_(self, obj):
        return obj.room.title

    room_.short_description = _('اتاق')

    def j_date_add(self, obj):
        return datetime2jalali(obj.date_add).strftime('%Y-%m-%d')

    j_date_add.short_description = _('تاریخ ایجاد')

class Discount_roomInline(admin.TabularInline):
    model = Discount_room
    max_num = 0
    extra = 0
    list_display = ('room', 'reduction',)
    readonly_fields = ('room',)


class DiscountAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    model = Discount
    autocomplete_fields = ('hotel',)
    def get_form(self, request, obj=None, **kwargs):
        form = super(DiscountAdmin, self).get_form(request, obj, **kwargs)
        field = form.base_fields["hotel"]
        field.widget.can_add_related = False
        field.widget.can_change_related = False
        field.widget.can_delete_related = False
        return form
    list_select_related = ('hotel',)
    search_fields = ['hotel__name', 'title']
    list_filter = ('active', 'reduction_type',)
    readonly_fields = ('flag_pricing',)
    inlines = (Discount_roomInline,)
    list_display = (
        'title', 'hotel', 'reduction_type', 'reduction', 'j_start_date', 'j_end_date', 'active', 'j_date_add')

    def hotel(self, obj):
        return obj.hotel.name

    def j_start_date(self, obj):
        return datetime2jalali(obj.start_date).strftime('%Y-%m-%d')

    j_start_date.short_description = _('تاریخ شروع')

    def j_end_date(self, obj):
        return datetime2jalali(obj.end_date).strftime('%Y-%m-%d')

    j_end_date.short_description = _('تاریخ پایان')

    def j_date_add(self, obj):
        return datetime2jalali(obj.date_add).strftime('%Y-%m-%d')

    j_date_add.short_description = _('تاریخ ایجاد')


admin.site.register(Calender_pricing, Calender_pricingAdmin)
admin.site.register(Calender_quantity, Calender_quantityAdmin)
admin.site.register(Cover, CoverAdmin)
admin.site.register(Room_cover, Room_coverAdmin)
# admin.site.register(Room_images, Room_imagesAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Discount, DiscountAdmin)

admin.site.register(Reviews, ReviewsAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Close_spots, Close_spotsAdmin)
admin.site.register(Room_facility, Room_facilityAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(Hotel, HotelAdmin)
