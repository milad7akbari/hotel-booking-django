from django.contrib import admin
from jalali_date import datetime2jalali

from apps.hotel.models import Cover, Hotel, Facility, Close_spots, Images, Check_in_out_rate, \
    Extra_person_rate, Room_cover, Room_facility, Room_images, Room, Reviews, Discount
from django.utils.translation import gettext_lazy as _


class ImagesInline(admin.TabularInline):
    model = Images
    extra = 1
    show_change_link = True


class Check_in_out_rateInline(admin.TabularInline):
    model = Check_in_out_rate
    extra = 1
    show_change_link = True


class Extra_person_rateInline(admin.TabularInline):
    model = Extra_person_rate
    extra = 1
    show_change_link = True


class DiscountInline(admin.TabularInline):
    model = Discount
    extra = 1
    show_change_link = True


class RoomInline(admin.TabularInline):
    model = Room
    extra = 0
    list_display = ('title', 'note', 'number_floor', 'count', 'capacity', 'extra_person', 'active')
    show_change_link = True


class HotelAdmin(admin.ModelAdmin):
    search_fields = ['name']
    model = Hotel
    list_filter = ('active', 'stars')
    list_display = ('name', 'reference', 'stars', 'active', 'date_add')
    readonly_fields = ('reference',)
    inlines = [DiscountInline, RoomInline, ImagesInline, Check_in_out_rateInline, Extra_person_rateInline]


class RoomAdmin(admin.ModelAdmin):
    model = Room
    search_fields = ['title', 'hotel__name']
    list_filter = ('active', 'capacity', 'count', 'capacity')
    list_select_related = ('hotel',)

    list_display = ('title', 'hotel', 'note', 'number_floor', 'count', 'capacity', 'extra_person', 'active')


class CoverAdmin(admin.ModelAdmin):
    model = Cover
    list_display = ('pk', 'note', 'title', 'file', 'active', 'date_add')
    search_fields = ['title', 'note']
    list_filter = ('active',)


class FacilityAdmin(admin.ModelAdmin):
    model = Facility
    list_select_related = ('hotel',)
    search_fields = ['hotel__name', 'title']
    list_filter = ('active',)
    list_display = ('hotel', 'title', 'active', 'date_add')


class Close_spotsAdmin(admin.ModelAdmin):
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
    list_display = ('hotel', 'file', 'title', 'active', 'date_add')
    list_select_related = ('hotel',)
    search_fields = ['hotel__name', 'title']
    list_filter = ('active',)

    def hotel(self, obj):
        return obj.hotel.name

    hotel.short_description = _('هتل')


class Room_coverAdmin(admin.ModelAdmin):
    model = Room_cover
    list_display = ('title', 'file', 'room', 'note', 'active', 'date_add')
    list_select_related = ('room',)
    search_fields = ['room__title', 'title', 'note']
    list_filter = ('active',)

    def room(self, obj):
        return obj.room.title

    room.short_description = _('اتاق')


class Room_imagesAdmin(admin.ModelAdmin):
    model = Room_images
    list_select_related = ('room',)
    search_fields = ['room__title', 'title']
    list_filter = ('active',)
    list_display = ('room', 'title', 'note', 'active', 'date_add')

    def room(self, obj):
        return obj.room.title

    room.short_description = _('اتاق')


class Room_facilityInline(admin.TabularInline):
    model = Room_facility
    list_display = ('hotel', 'title', 'active', 'date_add')


class ReviewsAdmin(admin.ModelAdmin):
    model = Reviews
    list_display = ('hotel', 'user', 'stars', 'title', 'active', 'j_date_add')
    list_select_related = ('hotel', 'user',)
    search_fields = ['hotel__name', 'title']
    list_filter = ('active', 'stars',)

    def hotel(self, obj):
        return obj.hotel.name
    hotel.short_description = _('هتل')

    def user(self, obj):
        return obj.user.name
    user.short_description = _('مشتری')

    def j_date_add(self, obj):
        return datetime2jalali(obj.date_add).strftime('%Y-%m-%d')
    j_date_add.short_description = _('تاریخ ایجاد')


class Room_facilityAdmin(admin.ModelAdmin):
    model = Room_facility
    list_display = ('room_', 'title', 'note', 'active', 'j_date_add',)
    list_select_related = ('room',)
    search_fields = ['room__title', 'title', 'note']
    list_filter = ('active',)

    def room_(self, obj):
        return obj.room.title

    room_.short_description = _('اتاق')

    def j_date_add(self, obj):
        return datetime2jalali(obj.date_add).strftime('%Y-%m-%d')

    j_date_add.short_description = _('تاریخ ایجاد')


class DiscountAdmin(admin.ModelAdmin):
    model = Discount
    list_select_related = ('hotel',)
    search_fields = ['hotel__name', 'title']
    list_filter = ('active', 'reduction_type',)
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


admin.site.register(Room_images, Room_imagesAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Discount, DiscountAdmin)
# admin.site.register(Room_cover, Room_coverAdmin)
# admin.site.register(Cover, CoverAdmin)

admin.site.register(Reviews, ReviewsAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Close_spots, Close_spotsAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(Room_facility, Room_facilityAdmin)
