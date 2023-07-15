from django.db import models

from apps.base.models import User
from apps.hotel.models import Hotel, Room


class Cart(models.Model):
    FLAG_CART = ((1, 'Pending'), (2, 'Done'), (3, 'Delete'),)
    user = models.ForeignKey(User, default=None, null=True, blank=True, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, default=None, on_delete=models.CASCADE)
    secure_key = models.CharField(null=False, blank=False, default=0, max_length=256)
    flag = models.SmallIntegerField(choices=FLAG_CART, null=False, default=1)
    date_upd = models.DateTimeField(auto_now=True)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return self.pk

    class Meta:
        verbose_name_plural = "Cart"
        verbose_name = "Cart"

    def __str__(self):
        return self.pk


class Cart_detail(models.Model):
    FLAG_CART = ((1, 'فعال'), (2, 'منقضی شد'), (3, 'پرداخت شده'),)
    cart = models.ForeignKey(Cart, default=None, on_delete=models.CASCADE , related_name='cart_detail')
    room = models.ForeignKey(Room, default=None, on_delete=models.CASCADE , related_name='cart_detail')
    quantity = models.SmallIntegerField(null=False, default=1)
    flag = models.SmallIntegerField(choices=FLAG_CART, null=False, default=1)
    date_add = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return self.pk

    class Meta:
        verbose_name_plural = "Cart Detail"
        verbose_name = "Cart Detail"

    def __str__(self):
        return self.pk
