"""membershipclub URL Configuration

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

from apps.front.views import getLoginForm, searchHotelCity, addToCartDetails, confirmation, registerNewUser, loginUser, \
    forgotPassword, forgotPasswordByToken, \
    forgotPasswordConfirm,  placeOrders, trackingSubmit, addCouponToCart

from apps.hotel.views import imagesHotel
from apps.customer.views import searchHotelCityQuick, searchHotelRoomsQuick

urlpatterns = [
    path('hotel-l/images/<str:ref>', imagesHotel),
    path('addCouponToCart/<int:cart_id>', addCouponToCart, name='addCouponToCart'),
    path('tracking-request/show', trackingSubmit, name='trackingSubmit'),
    path('hotel-l/search', searchHotelCity, name='searchHotelCity'),
    path('hotel-city', searchHotelCityQuick, name='searchHotelCityQuick'),
    path('hotel-rooms/<str:hotel_id>/<str:checkIn>/<str:checkOut>', searchHotelRoomsQuick, name='searchHotelRoomsQuick'),
    path('cart/place-order/<str:ref>/<int:cart_id>', placeOrders, name='placeOrders'),
    path('login/get-modal', getLoginForm),
    path('login/register-user', registerNewUser, name='registerNewUser'),
    path('login/login-user', loginUser, name='loginUser'),
    path('cart/add/<str:ref>/<int:id_cart>', addToCartDetails, name='addToCartDetails'),
    # path('createUser/<str:ref>/<int:id_cart>', createUserFromReservation, name='createUserFromReservation'),
    #path('get', cart, name='cart'),
    path('cart/confirmation/<str:reference>', confirmation, name='confirmation'),
    path('login/forgot-password', forgotPassword, name='forgotPassword'),
    path('login/forgot-pass/<str:token>', forgotPasswordByToken, name='forgotPasswordByToken'),
    path('login/forgot-pass-confirm', forgotPasswordConfirm, name='forgotPasswordConfirm')
]