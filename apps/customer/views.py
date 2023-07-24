from django.shortcuts import render

from apps.front.models import Order


# Create your views here.
def voucher(request):
    context = {}
    return render(request, 'customer/voucher.html', context)

def panelOrders(request):
    orders = Order.objects.filter(user=request.user).select_related('hotel')
    context = {
        'orders' : orders
    }
    return render(request, 'customer/orders.html', context)

def quickReserve(request):
    context = {}
    return render(request, 'customer/quick-reservation.html', context)
