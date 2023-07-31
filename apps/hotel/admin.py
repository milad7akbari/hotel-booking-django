from django.contrib import admin

from apps.hotel.models import Cover, Hotel, Facility, Close_spots, Images, Check_in_out_rate, \
    Extra_person_rate, Room_cover, Room_facility, Room_images, Room, Reviews, Discount


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
    list_display = ('title', 'note', 'number_floor', 'count', 'capacity', 'extra_person', 'active')
    show_change_link = True

class HotelAdmin(admin.ModelAdmin):
    search_fields = ['name']
    model = Hotel
    list_display = ('name', 'reference', 'stars', 'active', 'date_add')
    readonly_fields = ('reference',)
    inlines = [DiscountInline,RoomInline,ImagesInline, Check_in_out_rateInline, Extra_person_rateInline]



class RoomAdmin(admin.ModelAdmin):
    model = Room
    list_display = ('title', 'note', 'number_floor', 'count', 'capacity', 'extra_person', 'active')

class CoverAdmin(admin.ModelAdmin):
    model = Cover
    list_display = ('pk', 'file', 'title', 'active', 'date_add')


class FacilityAdmin(admin.ModelAdmin):
    model = Facility
    list_display = ('hotel', 'title', 'active', 'date_add')


class Close_spotsAdmin(admin.ModelAdmin):
    model = Close_spots
    list_display = ('hotel', 'short_desc', 'active', 'date_add')



class ImagesAdmin(admin.ModelAdmin):
    model = Images
    list_display = ('hotel', 'file', 'title', 'active', 'date_add')




class Room_imagesInline(admin.TabularInline):
    model = Room_images
    show_change_link = True


class Room_coverAdmin(admin.ModelAdmin):
    model = Room_cover


class Room_facilityInline(admin.TabularInline):
    model = Room_facility
    list_display = ('hotel', 'title', 'active', 'date_add')


class ReviewsAdmin(admin.ModelAdmin):
    model = Reviews
    list_display = ('title', 'short_desc', 'desc_bad', 'stars', 'desc_good', 'active', 'date_add')


class DiscountAdmin(admin.ModelAdmin):
    model = Discount
    list_display = ('title', 'room', 'reduction_type', 'reduction', 'start_date', 'end_date', 'active', 'date_add')
    def room(self, obj):
        return obj.room.title


admin.site.register(Room, RoomAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Room_cover, Room_coverAdmin)



admin.site.register(Reviews, ReviewsAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Close_spots, Close_spotsAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(Cover, CoverAdmin)
admin.site.register(Hotel, HotelAdmin)
