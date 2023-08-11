from django.contrib import admin

from apps.front.models import Cart_rule


class Cart_ruleAdmin(admin.ModelAdmin):
    model = Cart_rule
    list_filter = ('active',)
    list_display = ('title', 'reduction_type', 'reduction', 'start_date', 'end_date', 'active')
    readonly_fields = ('code',)


admin.site.register(Cart_rule, Cart_ruleAdmin)