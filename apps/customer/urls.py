"""hotel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from apps.customer.views import quickReserve, panelOrders, orderDetail, personality, editPersonality, \
    editPersonalityPassword, voucher

urlpatterns = [
    path('', panelOrders, name='panel'),
    path('edit-personality', editPersonality, name='editPersonality'),
    path('edit-personality-password', editPersonalityPassword, name='editPersonalityPassword'),
    path('personality', personality, name='personality'),
    path('voucher', voucher, name='voucher'),
    path('quick-reservation', quickReserve, name='quickReserve'),
    path('panel-orders/<str:type>', panelOrders, name='panelOrders'),
    path('order/<int:id>', orderDetail, name='orderDetail'),
]

