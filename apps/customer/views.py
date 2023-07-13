from django.shortcuts import render

# Create your views here.
def voucher(request):
    context = {}
    return render(request, 'customer/voucher.html', context)

def panelOrders(request):
    context = {}
    return render(request, 'customer/orders.html', context)

def quickReserve(request):
    context = {}
    return render(request, 'customer/quick-reservation.html', context)
