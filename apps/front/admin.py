from django.contrib import admin
from jalali_date import datetime2jalali
from django.utils.translation import gettext_lazy as _

from apps.front.models import Order, Order_detail, Cart, Cart_detail


class Order_detailInline(admin.TabularInline):
    model = Order_detail
    list_display = (
    'room', 'name', 'quantity', 'check_in_flag', 'check_out_flag', 'extra_person_quantity', 'base_price',
    'total_price_dis_excl', 'total_price_dis_incl')
    readonly_fields = (
    'room', 'name', 'quantity', 'check_in_flag', 'check_out_flag', 'extra_person_quantity', 'base_price',
    'total_price_dis_excl', 'total_price_dis_incl')
    show_change_link = True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return False

    extra = 0

class Cart_detailInline(admin.TabularInline):
    model = Cart_detail
    list_select_related = ('cart' , 'room')

    list_display = ('cart', 'room', 'quantity', 'check_in_flag', 'check_out_flag', 'extra_person_quantity', 'flag', 'date_add')
    readonly_fields = ('cart', 'room', 'quantity', 'check_in_flag', 'check_out_flag', 'extra_person_quantity', 'flag', 'date_add')
    show_change_link = True
    def has_delete_permission(self, request, obj=None):
        return True
    def has_add_permission(self, request, obj=None):
        return False
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_select_related = ('cart' , 'hotel', 'user')
    list_display = (
        'user', 'total_amount', 'hotel', 'cart', 'reference', 'current_state', 'total_room', 'total_amount_dis_incl',
        'has_invoice',
        'agree_rule',
        'j_date_add')
    readonly_fields = (
        'user', 'payment_type', 'reference', 'cart', 'hotel', 'total_paid', 'check_in_out_rate', 'extra_person_rate',
        'total_amount_dis_excl', 'current_state', 'total_room', 'total_amount_dis_incl'
        , 'agree_rule', 'j_date_add')
    inlines = [Order_detailInline, ]

    def total_amount(self, obj):
        if obj.total_amount_dis_incl:
            return obj.total_amount_dis_incl
        else:
            return 'Not Available'

    def j_date_add(self, obj):
        return datetime2jalali(obj.date_add).strftime('%Y-%m-%d')

    j_date_add.short_description = _('تاریخ ایجاد')
    total_amount.short_description = _('مبلغ با تخفیف')

    def user(self, obj):
        return obj.user.username

    def hotel(self, obj):
        return obj.hotel.name

    def cart(self, obj):
        return obj.cart.pk


class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_select_related = ('hotel', 'user')
    list_filter = ('flag',)
    list_display = ('user', 'hotel', 'j_from', 'j_to',  'flag')
    readonly_fields = ('user', 'hotel', 'j_from', 'j_to', 'check_in', 'check_out', 'secure_key', 'flag')
    inlines = [Cart_detailInline, ]

    def user(self, obj):
        return obj.user.username

    def hotel(self, obj):
        return obj.hotel.name

    def j_from(self, obj):
        return datetime2jalali(obj.check_in).strftime('%Y-%m-%d')

    j_from.short_description = _('ورود شمسی')

    def j_to(self, obj):
        return datetime2jalali(obj.check_out).strftime('%Y-%m-%d')

    j_to.short_description = _('خروج شمسی')


admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
