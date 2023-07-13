from modeltranslation.translator import register, TranslationOptions

from .models import Main, Files, Category


@register(Main)
class MainTranslationOptions(TranslationOptions):
    fields = ('title', 'desc',)
    required_languages = ('en', 'fa')



@register(Files)
class FilesTranslationOptions(TranslationOptions):
    fields = ('title', 'note',)
    required_languages = ('en', 'fa')


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title', 'desc',)
    required_languages = ('en', 'fa')

