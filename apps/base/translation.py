from modeltranslation.translator import register, TranslationOptions

from .models import Slider, Meta


@register(Slider)
class SliderTranslationOptions(TranslationOptions):
    fields = ('title',)
    required_languages = ('en', 'fa')


# @register(Images)
# class ImagesTranslationOptions(TranslationOptions):
#     fields = ('title',)
#     required_languages = ('en', 'fa')

# @register(Hotel)
# class HotelTranslationOptions(TranslationOptions):
#     fields = ('title',)
#     required_languages = ('en', 'fa')


@register(Meta)
class MetaTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'keywords',)
    required_languages = ('en', 'fa')
