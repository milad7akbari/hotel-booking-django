
from django import template
from django.utils.translation import gettext_lazy as _

register = template.Library()

@register.filter(name='currentState')
def currentState(state):
    if state == 1:
        return _('در انتظار تایید')
    else:
        return _('تایید شد')
