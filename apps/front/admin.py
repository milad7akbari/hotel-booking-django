from smtplib import SMTPException

from django.contrib import admin
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from jalali_date import datetime2jalali
from django.utils.translation import gettext_lazy as _

from Hotel_Test import settings
from apps.front.models import Order, Order_detail, Cart, Cart_detail, PendingOrder, AcceptOrder
from modeltranslation.admin import TranslationAdmin

from apps.front.models import Cart_rule


class Order_detailInline(admin.TabularInline):
    model = Order_detail
    classes = ('collapse',)
    can_delete = False
    show_change_link = True
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
    classes = ('collapse',)
    can_delete = False
    show_change_link = True
    list_select_related = ('cart', 'room')

    list_display = (
        'cart', 'room', 'quantity', 'check_in_flag', 'check_out_flag', 'extra_person_quantity', 'flag', 'date_add')
    readonly_fields = (
        'cart', 'room', 'quantity', 'check_in_flag', 'check_out_flag', 'extra_person_quantity', 'flag', 'date_add')
    show_change_link = True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return False

    extra = 0


class Cart_ruleAdmin(TranslationAdmin):
    model = Cart_rule
    list_filter = ('active',)
    list_display = ('title', 'reduction_type', 'reduction', 'start_date', 'end_date', 'active')
    readonly_fields = ('code',)


class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_select_related = ('hotel', 'user')
    list_filter = ('flag',)
    list_display = ('user', 'hotel', 'j_from', 'j_to', 'flag')
    readonly_fields = ('user', 'hotel', 'j_from', 'j_to', 'check_in', 'check_out', 'secure_key', 'flag')
    inlines = [Cart_detailInline, ]
    classes = ('collapse',)
    can_delete = False
    show_change_link = True
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







class OrderAdmin(admin.ModelAdmin):
    model = Order
    def has_delete_permission(self, request, obj=None):
        return False
    list_select_related = ('cart', 'hotel', 'user')
    list_display = (
        'reference', 'user', 'user_fullname', 'has_breakfast_', 'total_amount_dis_incl', 'total_amount_dis_excl',
        'total_paid', 'hotel', 'cart', 'current_state', 'total_room',
        'has_invoice', 'agree_rule', 'j_date_add')
    readonly_fields = (
        'user', 'payment_type','has_invoice','current_state', 'reference', 'cart', 'hotel', 'total_paid', 'check_in_out_rate', 'extra_person_rate',
        'total_amount_dis_excl', 'total_room', 'total_amount_dis_incl', 'agree_rule', 'j_date_add')
    inlines = [Order_detailInline, ]
    classes = ('collapse', )
    can_delete = False
    show_change_link = True
    def user_fullname(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name

    def has_breakfast_(self, obj):
        return obj.hotel.has_breakfast == 1 and _('دارد') or _('ندارد')

    def j_date_add(self, obj):
        return datetime2jalali(obj.date_add).strftime('%Y-%m-%d')

    has_breakfast_.short_description = _('صبحانه')
    user_fullname.short_description = _('نام مشتری')
    j_date_add.short_description = _('تاریخ ایجاد')

    def user(self, obj):
        return obj.user.username

    def hotel(self, obj):
        return obj.hotel.name

    def cart(self, obj):
        return obj.cart.pk





class PendingOrderAdmin(OrderAdmin):
    actions = ['current_status_2']
    change_form_template = ''

    @admin.action(description=_("تایید کردن"))
    def current_status_2(modeladmin, request, queryset):
        queryset.update(current_state=2)
    list_display = (
        'reference', 'user', 'user_fullname', 'has_breakfast_', 'total_amount_dis_incl', 'total_amount_dis_excl',
        'total_paid', 'hotel', 'cart', 'current_state', 'status','status_2', 'total_room',
        'has_invoice', 'agree_rule', 'j_date_add')
    def status(self, obj):
        return False
    status.boolean = True
    status.short_description = _('تایید شد؟')
    def status_2(self, obj):
        return False
    status_2.boolean = True
    status_2.short_description = _('رسید بانکی؟')
    def get_queryset(self, request):
        return self.model.objects.filter(current_state__lte=1)
class AcceptOrderAdmin(OrderAdmin):
    actions = ["current_status_3",]
    @admin.action(description=_("ارسال رسید به هتل ها"))
    def current_status_3(modeladmin, request, queryset):
        subject = 'فراموشی پسورد هتل تیک'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ('milad07akbari@gmail.com',)
        html_version = 'email/receipt.html'
        html_message = render_to_string(html_version, {'link': 'link', })
        message = EmailMessage(subject, html_message, email_from, recipient_list)
        message.content_subtype = 'html'  # this is required because there is no plain text email version
        try:
            message.send()
            queryset.update(current_state=3)
        except SMTPException as e:
            return False
    list_display = (
        'reference', 'user', 'user_fullname', 'has_breakfast_', 'total_amount_dis_incl', 'total_amount_dis_excl',
        'total_paid', 'hotel', 'cart', 'current_state', 'status', 'status_2', 'total_room',
        'has_invoice', 'agree_rule', 'j_date_add')

    def status(self, obj):
        return True

    status.boolean = True
    status.short_description = _('تایید شد؟')

    def status_2(self, obj):
        if obj.current_state == 3:
            return True
        else:
            return False

    status_2.boolean = True
    status_2.short_description = _('رسید بانکی؟')
    def get_queryset(self, request):
        return self.model.objects.filter(current_state__gte=2)


admin.site.register(AcceptOrder, AcceptOrderAdmin)
admin.site.register(PendingOrder, PendingOrderAdmin)
admin.site.register(Cart_rule, Cart_ruleAdmin)
admin.site.register(Cart, CartAdmin)
