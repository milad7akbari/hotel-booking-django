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
    secure_key = models.CharField(null=False, blank=False, default=0, max_length=256)
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
    fullname = models.CharField(default=None, null=True, max_length=256)
    mobile = models.CharField(default=None, null=True, max_length=256)
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
    PAY_YTPE = ((1, 'فیش بانکی / کارت به کارت'), (2, 'درگاه بانکی'),)
    user = models.ForeignKey(User, default=None, null=True, on_delete=models.CASCADE, related_name='order')
    cart = models.OneToOneField(Cart, default=None, null=True, on_delete=models.CASCADE, related_name='order')
    hotel = models.ForeignKey(Hotel, default=None, null=True, on_delete=models.CASCADE, related_name='order')
    reference = models.CharField(null=True, max_length=256)
    current_state = models.SmallIntegerField(null=False, default=1)
    payment_type = models.SmallIntegerField(null=False, default=1)
    total_discount = models.DecimalField(null=True, max_digits=12, decimal_places=2)
    total_paid = models.DecimalField(null=True, max_digits=12, decimal_places=2)
    total_amount = models.DecimalField(null=True, max_digits=12, decimal_places=2)
    total_products = models.SmallIntegerField(null=False, default=1)
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
    order = models.ForeignKey(Order, default=None, null=True, blank=True, on_delete=models.CASCADE, related_name='step')
    room = models.ForeignKey(Room, default=None, null=True, blank=True, on_delete=models.CASCADE, related_name='step')
    name = models.CharField(null=False, default=1, max_length=256)
    quantity = models.SmallIntegerField(null=False, default=1)
    check_in_flag = models.SmallIntegerField(null=False, default=0)
    check_out_flag = models.SmallIntegerField(null=False, default=0)
    extra_person_quantity = models.SmallIntegerField(null=False, default=0)
    product_price = models.DecimalField(null=True, max_digits=12, decimal_places=2)
    reduction = models.DecimalField(null=True, max_digits=12, decimal_places=2)
    total_price_dis_incl = models.DecimalField(null=True, max_digits=12, decimal_places=2)
    total_price_dis_excl = models.DecimalField(null=True, max_digits=12, decimal_places=2)
    total_paid = models.DecimalField(null=True, max_digits=12, decimal_places=2)
    reduction_type = models.SmallIntegerField(null=False, default=1)
    total_products = models.SmallIntegerField(null=False)
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return self.pk

    class Meta:
        verbose_name_plural = _("جزئیات سفارش ها")
        verbose_name = _("جزئیات سفارش ها")

    def __str__(self):
        return self.pk
