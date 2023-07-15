import secrets
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.db.models import Count, Prefetch, Q
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from apps.base.models import User, Forgot_password, Slider, Meta, Cities
from apps.blog.models import Main
from apps.front.forms import forgotPasswordForm, registerUserFromReservationForm, loginUserForm, \
    forgotPasswordConfirmForm, registerGuestFromReservationForm, registerUser
from django.utils.translation import gettext_lazy as _

from apps.front.models import Cart, Cart_detail
from apps.hotel.models import Hotel, Room, Discount


def forgotPassword(request):
    if request.method == 'POST':
        status = 0
        msg = _('اطلاعاتی یافت نشد')
        form = forgotPasswordForm(request.POST)
        if form.is_valid():
            username_email = form.cleaned_data['username_email']
            if '@' in username_email:
                username = 0
                user = User.objects.get(email=username_email)
            else:
                username = 1
                user = User.objects.get(username=username_email)
            if user is not None:
                token = secrets.token_urlsafe()
                Forgot_password.objects.create(user_id=user.id, token=token)
                if username == 1:
                    #   url = request.get_host() + reverse('forgotPasswordByToken', kwargs={'token': 'qwddqdqwdqwd'})
                    msg = _('لینک بازیابی پسورد به موبایل شما ارسال شد! ')
                else:
                    msg = _('لینک بازیابی پسورد به ایمیل شما ارسال شد! ')
                status = 1
        else:
            status = -1
        context = {
            "status": status,
            "msg": msg,
        }
        return JsonResponse(context)


def forgotPasswordByToken(request, token):
    # if chk is not None:
    form = forgotPasswordConfirmForm()
    context = {
        'form': form,
        'token': token,
    }
    return render(request, '_partial/forgot-password-confirm.html', context)


def searchHotelCity(request):
    filter_param = request.GET.get("filter")
    title_param = request.GET.get("title")
    if filter_param is not None:
        if title_param is not None:
            hotel = Cities.objects.filter(hotel__isnull=False, name__contains=title_param).annotate(
                count=Count('name')).values('name')
            if not hotel.count():
                hotel = Hotel.objects.filter(active=1, name__contains=title_param).annotate(
                    count=Count('city__name')).values('name')
            context = {
                'hotel': list(hotel),
            }
            return JsonResponse(context)
        else:
            return None
    else:
        return None


def forgotPasswordConfirm(request):
    path = request.get_full_path()
    msg = _('مشکل در بروزرسانی اطلاعات')
    # token_url = re.sub(r'.*\/', '', path)
    token_form = request.POST['token']
    if request.method == 'POST':
        user_token = Forgot_password.objects.filter(token=token_form).first()
        if user_token is not None:
            user = User.objects.get(pk=user_token.user_id)
            form = forgotPasswordConfirmForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                status = 1
                user_token.status = status
                user_token.save()
                msg = _('تغییر پسورد موفقیت آمیز بود')
            else:
                status = -1
        else:
            status = -1
        context = {
            'status': status,
            'msg': msg,
        }
        return JsonResponse(context)


def home_page(request):
    slider = Slider.objects.filter(active=1).order_by('?')[:3]
    meta = Meta.objects.first()
    blogs_related = Main.objects.filter(active=1).select_related('default_image').values(
        'pk',
        'title',
        'desc',
        'date_upd',
        'default_image__file').order_by('?')[:7]
    context = {
        'blogs_related': blogs_related,
        'slider': slider,
        'meta': meta,
    }
    return render(request, 'pages/home.html', context)


def confirmation(request):
    context = {}
    return render(request, 'pages/confirmation.html', context)


def dandal(request):
    context = {}
    return render(request, 'pages/dandal.html', context)


def cart(request, ref):
    hotel = get_object_or_404(Hotel, reference=ref)
    if request.session.session_key:
        session_key = request.session.session_key
        cart = Cart.objects.filter(secure_key=session_key, flag=1, hotel_id=hotel.pk)
        if cart.exists():
            cart = cart.prefetch_related(Prefetch(
            'cart_detail',
            queryset=Cart_detail.objects.filter(flag=1).select_related('room', 'room__default_cover').prefetch_related('room__room_facility_set','room__room_images_set',Prefetch(
            'room__room_discount',
            queryset=Discount.objects.filter(Q(active=1) & Q(start_date__lt=timezone.now()) & Q(end_date__gt=timezone.now())).distinct())))).all()
        else:
            return redirect(reverse('hotelCategory'))
        context = {
            'cart': cart,
            'form': registerUserFromReservationForm,
            'form_1': registerGuestFromReservationForm
        }
        return render(request, 'pages/cart.html', context)


def addToCart(request, ref):
    if request.method == 'POST':
        if not request.session.session_key:
            request.session.save()
        session_key = request.session.session_key
        hotel = get_object_or_404(Hotel, reference=ref)
        if request.user.is_authenticated:
            cart_check = Cart.objects.filter(user_id=request.user.pk, hotel_id=hotel.pk)
        else:
            cart_check = Cart.objects.filter(secure_key=session_key, hotel_id=hotel.pk)

        if not cart_check.exists():
            if request.user.is_authenticated:
                cart_check = Cart(hotel_id=hotel.pk, user_id=request.user.pk, secure_key=session_key)
            else:
                cart_check = Cart(hotel_id=hotel.pk, secure_key=session_key)
            cart_check.save()
        else:
            cart_check = cart_check.first()
        Cart_detail.objects.filter(cart_id=cart_check.pk).update(flag=3)
        flag = False
        if request.POST.getlist('qty[]') and request.POST.getlist('room[]'):
            for idx, qty in enumerate(request.POST.getlist('qty[]')):
                if qty.isdigit() and int(qty) > 0:
                    room_id = request.POST.getlist('room[]')[idx]
                    if room_id.isdigit() and int(room_id) > 0:
                        check = Room.objects.filter(pk=room_id, hotel_id=hotel.pk).exists()
                        if check:
                            cart_detail = Cart_detail(cart_id=cart_check.pk, room_id=room_id, quantity=qty)
                            cart_detail.save()
                            flag = True
            if flag:
                return redirect(reverse('cart', kwargs={'ref': ref}))
        else:
            referer = request.META.get("HTTP_REFERER")
            return HttpResponseRedirect(referer)


def getLoginForm(request, *args, **kwargs):
    if not request.user.is_authenticated:
        if request.GET.get("modalName") == 'login-pass':
            login_password = loginUserForm()
            context = {
                'form': login_password
            }
            return render(request, '_partial/modal/register/login-password.html', context)
        elif request.GET.get("modalName") == 'forgot-passwd':
            forgot_password = forgotPasswordForm()
            context = {
                'form': forgot_password
            }
            return render(request, '_partial/modal/register/forgot-password.html', context)
        elif request.GET.get("modalName") == 'register-new':
            register = registerUser()
            context = {
                'form': register
            }
            return render(request, '_partial/modal/register/register-user.html', context)
    else:
        return render(request, 'errors/404.html', {})


def registerNewUser(request):
    if request.method == 'POST':
        form = registerUser(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            context = {
                "result": _('ثبت نام موفقیت آمیز بود!'),
                "err": False,
            }
            return JsonResponse(context)
        else:
            if 'err' in form.errors:
                err = True
                context = {
                    "result": form.errors,
                    "err": err,
                }
                return JsonResponse(context)


def loginUser(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = loginUserForm(data=request.POST)
            if form.is_valid():
                username_email = form.cleaned_data['username']
                password = make_password(form.cleaned_data['password'], salt="Argon2PasswordHasher", hasher="default")
                if '@' in username_email:
                    user = User.objects.filter(email=username_email, password=password).first()
                else:
                    if len(username_email) == 10:
                        username_email = '09' + username_email[1:]
                    user = User.objects.filter(username=username_email, password=password).first()
                if user is not None:
                    status = 1
                    login(request, user)
                else:
                    status = 0
            else:
                status = -1

            context = {
                "status": status,
            }
            return JsonResponse(context)
