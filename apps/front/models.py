from django.contrib.auth.hashers import make_password
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User
from apps.hotel.models import Hotel, Room


class Cart(models.Model):
    FLAG_CART = ((1, _('در انتظار تکمیل')), (2, _('سفارش')), (3, _('حذف')),)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,verbose_name=_('مشتری'))
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, blank=True, null=True,verbose_name=_('هتل'))
    check_in = models.DateField(default=None, null=True, blank=True,verbose_name=_('ورود'))
    check_out = models.DateField(default=None, null=True, blank=True,verbose_name=_('خروج'))
    secure_key = models.CharField(null=False, blank=False, default=0, max_length=255,verbose_name=_('کد'))
    flag = models.SmallIntegerField(choices=FLAG_CART, null=False, default=1,verbose_name=_('فلگ'))
    date_upd = models.DateTimeField(auto_now=True,verbose_name=_('تاریخ آپدیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True,verbose_name=_('تاریخ ایجاد'))

    def __unicode__(self):
        return self.pk

    class Meta:
        verbose_name_plural = _("کارت")
        verbose_name = _("کارت")

    def __str__(self):
        return str(self.pk)


class Cart_detail(models.Model):
    FLAG = ((1, 'Yes'), (0, 'No'),)
    FLAG_CART = ((1, _('فعال')), (2, _('منقضی شد')), (3, _('پرداخت شده')),)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, blank=True, null=True, related_name='cart_detail',verbose_name=_('کارت'))
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, blank=True, null=True, related_name='cart_detail',verbose_name=_('اتاق'))
    quantity = models.SmallIntegerField(null=False, default=1,verbose_name=_('تعداد'))
    check_in_flag = models.SmallIntegerField(choices=FLAG, null=False, default=0,verbose_name=_('ورود زود هنگام'))
    check_out_flag = models.SmallIntegerField(choices=FLAG, null=False, default=0,verbose_name=_('خروج دیر هتگام'))
    extra_person_quantity = models.SmallIntegerField(null=False, default=0,verbose_name=_('نفر اضافه'))
    flag = models.SmallIntegerField(choices=FLAG_CART, null=False, default=1,verbose_name=_('فلگ'))
    date_add = models.DateTimeField(auto_now_add=True, null=True,verbose_name=_('تاریخ ایجاد'))

    def __unicode__(self):
        return self.pk

    class Meta:
        verbose_name_plural = _("جزئیات کارت")
        verbose_name = _("جزئیات کارت")

    def __str__(self):
        return str(self.pk)


class Cart_guest(models.Model):
    FLAG = ((2, 'Done'), (3, 'Delete'),)
    NATIONALITY = ((1, _('ایرانی')), (2, _('غیر ایرانی')),)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, blank=True, null=True, related_name='cart_guest',verbose_name=_('اتاق'))
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, blank=True, null=True, related_name='cart_guest',verbose_name=_('کارت'))
    cart_detail = models.ForeignKey(Cart_detail, on_delete=models.SET_NULL, blank=True, null=True, related_name='cart_guest',verbose_name=_('جزئیات کارت'))
    fullname = models.CharField(default=None, null=True, max_length=255,verbose_name=_('نام کامل'))
    mobile = models.CharField(default=None, null=True, max_length=255,verbose_name=_('موبایل'))
    nationality = models.SmallIntegerField(choices=NATIONALITY, null=True,verbose_name=_('ملیت'))
    flag = models.SmallIntegerField(choices=FLAG, null=False, default=1,verbose_name=_('فلگ'))
    date_upd = models.DateTimeField(auto_now=True,verbose_name=_('تاریخ آپدیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True,verbose_name=_('تاریخ ایجاد'))

    def __unicode__(self):
        return str(self.fullname)

    class Meta:
        verbose_name_plural = _("مسافر")
        verbose_name = _("مسافر")

    def __str__(self):
        return str(self.fullname)



class Step(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.SET_NULL, blank=True, null=True, related_name='step')
    step = models.SmallIntegerField(null=False, default=1)
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return self.step


class Order(models.Model):
    YES_NO = ((True, 'دارم'), (False, 'ندارم'),)
    PTYPE = ((1, 'رزرو'), (2, 'فیش بانکی'), (3, 'آنلاین'),)
    CURRENTSTATE = ((1, 'در انتظار تایید'), (2, 'تایید شد'), (3, 'ارسال رسید به هتل ها'),)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='order',verbose_name=_('مشتری'))
    cart = models.OneToOneField(Cart, on_delete=models.SET_NULL, blank=True, null=True, related_name='order',verbose_name=_('سبد'))
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, blank=True, null=True, related_name='order',verbose_name=_('هتل'))
    reference = models.CharField(null=True, max_length=255,verbose_name=_('رفرنس'))
    current_state = models.SmallIntegerField(choices=CURRENTSTATE,null=False, default=1,verbose_name=_('وضعیت فعلی'))
    payment_type = models.SmallIntegerField(choices=PTYPE,null=False, default=1,verbose_name=_('نوع پرداخت'))
    total_paid = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=2,verbose_name=_('مبلغ پرداخت شده'))
    check_in = models.DateField(default=None, null=True, blank=True,verbose_name=_('ورود'))
    check_out = models.DateField(default=None, null=True, blank=True,verbose_name=_('خروج'))
    check_in_out_rate = models.DecimalField(null=True, max_digits=12, decimal_places=2,verbose_name=_('مبلغ ورود و خروح'))
    extra_person_rate = models.DecimalField(null=True, max_digits=12, decimal_places=2,verbose_name=_('مبلغ نفر اضافه'))
    total_amount_dis_excl = models.DecimalField(null=True, max_digits=12, decimal_places=2,verbose_name=_('قیمت بدون تخفیف'))
    total_amount_dis_incl = models.DecimalField(null=True, max_digits=12, decimal_places=2,verbose_name=_('قیمت با تخفیف'))
    total_room = models.SmallIntegerField(null=False, default=1,verbose_name=_('تعدا اتاق'))
    has_invoice = models.BooleanField(choices=YES_NO, null=True, blank=True, default=None,verbose_name=_('فاکتور رسمی'))
    agree_rule = models.BooleanField(choices=YES_NO, null=True, blank=True, default=None,verbose_name=_('قبول قوانین'))
    date_upd = models.DateTimeField(auto_now=True,verbose_name=_('تاریخ آپدیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True,verbose_name=_('تاریخ ایجاد'))

    def __unicode__(self):
        return self.pk

    class Meta:
        verbose_name_plural = _("سفارش ها")
        verbose_name = _("سفارش ها")

    def __str__(self):
        return str(self.pk)
class PendingOrder(Order):
    class Meta:
        proxy = True
        verbose_name = _("رزرو موقت")
        verbose_name_plural = _("رزرو موقت")


class AcceptOrder(Order):
    class Meta:
        proxy = True
        verbose_name = _("رزرو تایید شده")
        verbose_name_plural = _("رزرو تایید شده")

class Order_detail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True,related_name='order_detail',verbose_name=_('سفارش'))
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, blank=True, null=True,related_name='order_detail',verbose_name=_('اتاق'))
    name = models.CharField(null=False, default=1, max_length=255,verbose_name=_('نام'))
    quantity = models.SmallIntegerField(null=False, default=1,verbose_name=_('تعداد'))
    check_in_flag = models.SmallIntegerField(null=False, default=0,verbose_name=_('ورود زود هنگام'))
    check_out_flag = models.SmallIntegerField(null=False, default=0,verbose_name=_('خروج دیر هنگام'))
    extra_person_quantity = models.SmallIntegerField(null=False, default=0,verbose_name=_('افراد اضافه'))
    base_price = models.DecimalField(null=True, max_digits=12, decimal_places=2,verbose_name=_('فیمت پایه'))
    total_price_dis_excl = models.DecimalField(null=True, max_digits=12, decimal_places=2,verbose_name=_('قیمت بدون تخفیف'))
    total_price_dis_incl = models.DecimalField(null=True, max_digits=12, decimal_places=2,verbose_name=_('قیمت با تخفیف'))
    date_upd = models.DateTimeField(auto_now=True,verbose_name=_('تاریخ اپدیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True,verbose_name=_('تاریخ ایجاد'))


    def __unicode__(self):
        return self.pk

    class Meta:
        verbose_name_plural = _("جزئیات سفارش ها")
        verbose_name = _("جزئیات سفارش ها")

    def __str__(self):
        return str(self.pk)


class Order_detail_guest(models.Model):
    FLAG = ((2, 'Done'), (3, 'Delete'),)
    NATIONALITY = ((1, _('ایرانی')), (2, _('غیر ایرانی')),)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, blank=True, null=True, related_name='order_detail_guest',verbose_name=_('اتاق'))
    order_detail = models.ForeignKey(Order_detail, on_delete=models.SET_NULL, blank=True, null=True, related_name='order_detail_guest',verbose_name=_('جزئیات سفارش'))
    fullname = models.CharField(default=None, null=True, max_length=255,verbose_name=_('نام کامل'))
    mobile = models.CharField(default=None, null=True, max_length=255,verbose_name=_('موبایل'))
    nationality = models.SmallIntegerField(choices=NATIONALITY, null=True,verbose_name=_('ملیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True,verbose_name=_('تاریخ ایجاد'))

    def __unicode__(self):
        return str(self.fullname)

    class Meta:
        verbose_name_plural = _("مسافر")
        verbose_name = _("مسافر")

    def __str__(self):
        return str(self.fullname)


class Cart_rule(models.Model):
    def save(self, *args, **kwargs):
        replacers = {'$', "/", "+", "="}
        ref = make_password(str(self.pk), salt="Argon2PasswordHasher", hasher="default")
        for r in replacers:
            ref = ref.replace(r, '')
        self.code = ref[-7:]
        super(Cart_rule, self).save(*args, **kwargs)
    TYPE_DISCOUNT = ((1, 'درصد'), (2, 'مقدار'),)
    YES_NO = ((1, 'Yes'), (2, 'No'),)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, verbose_name=_("عنوان تخفیف"))
    code = models.CharField(max_length=255, blank=True, verbose_name=_("کد تخفیف"))
    start_date = models.DateTimeField(default=0, null=True, verbose_name=_("تاریخ شروع"))
    end_date = models.DateTimeField(default=0, null=True, verbose_name=_("تاریخ پایان"))
    quantity = models.SmallIntegerField(default=0, null=True, verbose_name=_("موجودی"))
    minimum_amount = models.DecimalField(null=True, max_digits=12, decimal_places=2, verbose_name=_("حداقل مبلغ خرید"))
    reduction_type = models.SmallIntegerField(choices=TYPE_DISCOUNT,null=False, default=1, verbose_name=_("نوع تخفیف"))
    reduction = models.DecimalField(null=True, max_digits=12, decimal_places=2, default=0, verbose_name=_("مقدار"))
    highlight = models.SmallIntegerField(choices=YES_NO,null=False, default=0, verbose_name=_("نمایان برای مشتری"))
    active = models.SmallIntegerField(choices=YES_NO,null=False, default=1, verbose_name=_("فعال"))
    date_upd = models.DateTimeField(auto_now=True ,verbose_name=_('تاریخ اپدیت'))
    date_add = models.DateTimeField(auto_now_add=True, null=True ,verbose_name=_('تاریخ ایجاد'))

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name_plural = _('تخفیف مشتریان')
        verbose_name = _('تخفیف مشتریان')

    def __unicode__(self):
        return str(self.title)

class Order_cart_rule(models.Model):
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, blank=True, null=True)
    cart_rule = models.ForeignKey(Cart_rule, on_delete=models.SET_NULL, blank=True, null=True)
    value = models.DecimalField(null=True, max_digits=12, decimal_places=2, verbose_name=_("حداقل مبلغ خرید"))
    date_add = models.DateTimeField(auto_now_add=True, null=True,verbose_name=_('تاریخ ایجاد'))

    def __str__(self):
        return str(self.value)

    class Meta:
        verbose_name_plural = _('تخفیفات ثبت شده')
        verbose_name = _('تخفیفات ثبت شده')

    def __unicode__(self):
        return str(self.value)

class Cart_cart_rule(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.SET_NULL, blank=True, null=True)
    cart_rule = models.ForeignKey(Cart_rule, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return str(self.cart.pk)

    class Meta:
        verbose_name_plural = _('تخفیف مشتریان')
        verbose_name = _('تخفیف مشتریان')

    def __unicode__(self):
        return str(self.cart.pk)
