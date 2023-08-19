from modeltranslation.translator import register, TranslationOptions

from apps.front.models import Cart_rule


@register(Cart_rule)
class Cart_ruleTranslationOptions(TranslationOptions):
    fields = ('title',)
    required_languages = ('en', 'fa')

