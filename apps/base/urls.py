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
    forgotPasswordConfirm, createUserFromReservation

from apps.hotel.views import imagesHotel


urlpatterns = [
    path('images/<str:ref>', imagesHotel),
    path('search', searchHotelCity, name='searchHotelCity'),
    path('get-modal', getLoginForm),
    path('register-user', registerNewUser, name='registerNewUser'),
    path('login-user', loginUser, name='loginUser'),
    path('add/<str:ref>', addToCartDetails, name='add'),
    path('createUser/<str:ref>/<int:id_cart>', createUserFromReservation, name='createUserFromReservation'),
    #path('get', cart, name='cart'),
    path('confirmation', confirmation, name='confirmation'),
    path('forgot-password', forgotPassword, name='forgotPassword'),
    path('forgot-pass/<str:token>', forgotPasswordByToken, name='forgotPasswordByToken'),
    path('forgot-pass-confirm', forgotPasswordConfirm, name='forgotPasswordConfirm')
]