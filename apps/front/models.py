from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User
from apps.hotel.models import Hotel, Room


class Cart(models.Model):
    FLAG_CART = ((1, 'Pending'), (2, 'Done'), (3, 'Delete'),)
    user = models.ForeignKey(User, default=None, null=True, blank=True, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, default=None, on_delete=models.CASCADE)
    check_in = models.DateField(default=None, null=True, blank=True)
    check_out = models.DateField(default=None, null=True, blank=True)
    secure_key = models.CharField(null=False, blank=False, default=0, max_length=255)
    flag = models.SmallIntegerField(choices=FLAG_CART, null=False, default=1)
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return self.pk

    class Meta:
        verbose_name_plural = _("کارت")
        verbose_name = _("کارت")

    def __str__(self):
        return self.pk


class Cart_detail(models.Model):
    FLAG = ((1, 'Yes'), (0, 'No'),)
    FLAG_CART = ((1, 'فعال'), (2, 'منقضی شد'), (3, 'پرداخت شده'),)
    cart = models.ForeignKey(Cart, default=None, on_delete=models.CASCADE, related_name='cart_detail')
    room = models.ForeignKey(Room, default=None, on_delete=models.CASCADE, related_name='cart_detail')
    quantity = models.SmallIntegerField(null=False, default=1)
    check_in_flag = models.SmallIntegerField(choices=FLAG, null=False, default=0)
    check_out_flag = models.SmallIntegerField(choices=FLAG, null=False, default=0)
    extra_person_quantity = models.SmallIntegerField(null=False, default=0)
    flag = models.SmallIntegerField(choices=FLAG_CART, null=False, default=1)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return self.pk

    class Meta:
        verbose_name_plural = _("جزئیات کارت")
        verbose_name = _("جزئیات کارت")

    def __str__(self):
        return self.pk


class Guest(models.Model):
    FLAG = ((2, 'Done'), (3, 'Delete'),)
    NATIONALITY = ((1, _('ایرانی')), (2, _('غیر ایرانی')),)
    room = models.ForeignKey(Room, default=None, null=True, blank=True, on_delete=models.CASCADE, related_name='guest')
    cart_detail = models.ForeignKey(Cart_detail, default=None, null=True, blank=True, on_delete=models.CASCADE,
                                    related_name='guest')
    fullname = models.CharField(default=None, null=True, max_length=255)
    mobile = models.CharField(default=None, null=True, max_length=255)
    nationality = models.SmallIntegerField(choices=NATIONALITY, null=True)
    flag = models.SmallIntegerField(choices=FLAG, null=False, default=1)
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return self.pk

    class Meta:
        verbose_name_plural = _("مسافر")
        verbose_name = _("مسافر")

    def __str__(self):
        return self.pk


class Step(models.Model):
    cart = models.OneToOneField(Cart, default=None, null=True, blank=True, on_delete=models.CASCADE,
                                related_name='step')
    step = models.SmallIntegerField(null=False, default=1)
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return self.step


class Order(models.Model):
    YES_NO = ((True, 'دارم'), (False, 'ندارم'),)
    PTYPE = ((1, 'رزرو'), (2, 'فیش بانکی'), (3, 'آنلاین'),)
    CURRENTSTATE = ((1, 'در انتظار تایید'), (2, 'تایید از سوی کارمندان'),)
    user = models.ForeignKey(User, default=None, null=True, on_delete=models.CASCADE, related_name='order')
    cart = models.OneToOneField(Cart, default=None, null=True, on_delete=models.CASCADE, related_name='order')
    hotel = models.ForeignKey(Hotel, default=None, null=True, on_delete=models.CASCADE, related_name='order')
    reference = models.CharField(null=True, max_length=255)
    current_state = models.SmallIntegerField(choices=CURRENTSTATE,null=False, default=1)
    payment_type = models.SmallIntegerField(choices=PTYPE,null=False, default=1)
    total_paid = models.DecimalField(null=True, max_digits=12, decimal_places=2)
    check_in_out_rate = models.DecimalField(null=True, max_digits=12, decimal_places=2)
    extra_person_rate = models.DecimalField(null=True, max_digits=12, decimal_places=2)
    total_amount_dis_excl = models.DecimalField(null=True, max_digits=12, decimal_places=2)
    total_amount_dis_incl = models.DecimalField(null=True, max_digits=12, decimal_places=2)
    total_room = models.SmallIntegerField(null=False, default=1)
    has_invoice = models.BooleanField(choices=YES_NO, null=True, blank=True, default=None)
    agree_rule = models.BooleanField(choices=YES_NO, null=True, blank=True, default=None)
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return self.pk

    class Meta:
        verbose_name_plural = _("سفارش ها")
        verbose_name = _("سفارش ها")

    def __str__(self):
        return self.pk


class Order_detail(models.Model):
    order = models.ForeignKey(Order, default=None, null=True, blank=True, on_delete=models.CASCADE,related_name='order_detail')
    room = models.ForeignKey(Room, default=None, null=True, blank=True, on_delete=models.CASCADE,related_name='order_detail')
    name = models.CharField(null=False, default=1, max_length=255)
    quantity = models.SmallIntegerField(null=False, default=1)
    check_in_flag = models.SmallIntegerField(null=False, default=0)
    check_out_flag = models.SmallIntegerField(null=False, default=0)
    extra_person_quantity = models.SmallIntegerField(null=False, default=0)
    base_price = models.DecimalField(null=True, max_digits=12, decimal_places=2)
    total_price_dis_excl = models.DecimalField(null=True, max_digits=12, decimal_places=2)
    total_price_dis_incl = models.DecimalField(null=True, max_digits=12, decimal_places=2)
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return self.pk

    class Meta:
        verbose_name_plural = _("جزئیات سفارش ها")
        verbose_name = _("جزئیات سفارش ها")

    def __str__(self):
        return self.pk



class Cart_rule(models.Model):
    TYPE_DISCOUNT = ((1, 'درصد'), (2, 'مقدار'),)
    YES_NO = ((1, 'Yes'), (2, 'No'),)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0, null=True)
    title = models.CharField(max_length=255, blank=True, verbose_name=_("عنوان تخفیف"))
    code = models.CharField(max_length=255, blank=True, verbose_name=_("کد تخفیف"), unique=True)
    start_date = models.DateTimeField(default=0, null=True, verbose_name=_("تاریخ شروع"))
    end_date = models.DateTimeField(default=0, null=True, verbose_name=_("تاریخ پایان"))
    quantity = models.SmallIntegerField(default=0, null=True, verbose_name=_("موجودی"))
    minimum_amount = models.DecimalField(null=True, max_digits=12, decimal_places=2, verbose_name=_("حداقل مبلغ خرید"))
    reduction_type = models.SmallIntegerField(choices=TYPE_DISCOUNT,null=False, default=1, verbose_name=_("نوع تخفیف"))
    reduction = models.DecimalField(null=True, max_digits=12, decimal_places=2, default=0, verbose_name=_("مقدار"))
    highlight = models.SmallIntegerField(choices=YES_NO,null=False, default=0, verbose_name=_("نمایان برای مشتری"))
    active = models.SmallIntegerField(choices=YES_NO,null=False, default=1, verbose_name=_("فعال"))
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name_plural = _('تخفیف مشتریان')
        verbose_name = _('تخفیف مشتریان')

    def __unicode__(self):
        return str(self.title)

class Order_cart_rule(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, default=0, null=True)
    cart_rule = models.ForeignKey(Cart_rule, on_delete=models.CASCADE, null=True)
    value = models.DecimalField(null=True, max_digits=12, decimal_places=2, verbose_name=_("حداقل مبلغ خرید"))
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.value)

    class Meta:
        verbose_name_plural = _('تخفیفات ثبت شده')
        verbose_name = _('تخفیفات ثبت شده')

    def __unicode__(self):
        return str(self.value)

class Cart_cart_rule(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, null=True)
    cart_rule = models.ForeignKey(Cart_rule, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.cart.pk)

    class Meta:
        verbose_name_plural = _('تخفیف مشتریان')
        verbose_name = _('تخفیف مشتریان')

    def __unicode__(self):
        return str(self.cart.pk)
