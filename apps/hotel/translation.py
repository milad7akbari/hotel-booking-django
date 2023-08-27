from modeltranslation.translator import register, TranslationOptions

from apps.hotel.models import Hotel, Facility, Close_spots, Room, Room_facility


@register(Hotel)
class HotelTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'long_desc',
        'short_desc',
        'rule_cancelable',
        'rule_enter',
        'address',
        'meta_keywords',
    )
    required_languages = {'en': ('name', ) ,'default': ('name',)}



@register(Facility)
class FacilityTranslationOptions(TranslationOptions):
    fields = (
        'title',
    )


@register(Close_spots)
class Close_spotsTranslationOptions(TranslationOptions):
    fields = (
        'short_desc',
    )

@register(Room)
class RoomTranslationOptions(TranslationOptions):
    fields = (
        'title',
    )
    required_languages = ('en', 'fa')


@register(Room_facility)
class Room_facilityTranslationOptions(TranslationOptions):
    fields = (
        'title',
    )
    required_languages = ('en', 'fa')

