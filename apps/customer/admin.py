from django.contrib import admin

from apps.front.models import Cart_rule


class Cart_ruleAdmin(admin.ModelAdmin):
    model = Cart_rule
    list_display = ('title', 'reduction_type', 'reduction', 'start_date', 'end_date', 'active', 'date_add')


admin.site.register(Cart_rule, Cart_ruleAdmin)