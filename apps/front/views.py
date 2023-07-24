import secrets
import uuid

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Count, Prefetch, Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from apps.base.models import Forgot_password, Slider, Meta, Cities
from apps.blog.models import Main
from apps.front.forms import forgotPasswordForm, registerUserFromReservationForm, loginUserForm, \
    forgotPasswordConfirmForm, registerGuestFromReservationForm, registerUser, placeOrderForm
from django.utils.translation import gettext_lazy as _

from apps.front.models import Cart, Cart_detail, Guest, Step
from apps.hotel.models import Hotel, Room, Discount, Check_in_out_rate, Extra_person_rate


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
            flag = 1
            url = reverse('hotelCategory'),
            if not hotel.count():
                hotel = Hotel.objects.filter(active=1, name__contains=title_param).annotate(
                    count=Count('city__name')).values('name', 'reference').all()
                flag = 2
                url = reverse('hotelPage', kwargs={'reference': hotel.reference,'name': hotel.name}),

            context = {
                'flag': flag,
                'url': url,
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


def createUserFromReservation(request, ref, id_cart):
    if request.method == 'POST':
        form = registerUserFromReservationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            hotel = get_object_or_404(Hotel, reference=ref)
            cart = Cart.objects.filter(hotel_id=hotel.pk, pk=id_cart)
            if cart.exists():
                cart.update(user_id=request.user.pk)
            context = {
                "result": _('ورود اطلاعات موفقیت آمیز بود'),
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

def getInfoFromCart_(cart_pk, hotel_pk, flag = False):
    info = Cart.objects.filter(pk=cart_pk).select_related('user', 'hotel', 'hotel__extra_person_rate',
                                                          'hotel__check_in_out_rate').prefetch_related(
        Prefetch(
            'cart_detail',
            queryset=Cart_detail.objects.filter(flag=1).prefetch_related('room', 'guest')
        ), Prefetch(
            'cart_detail__room__room_discount',
            queryset=Discount.objects.filter(
                Q(active=1) & Q(start_date__lt=timezone.now()) & Q(end_date__gt=timezone.now()))
        )).all()
    if flag:
        extra_person = Extra_person_rate.objects.filter(hotel_id=hotel_pk, active=1).exists()
        check_in_out = Check_in_out_rate.objects.filter(hotel_id=hotel_pk, active=1).exists()
        for i in info:
            i.extra_person = extra_person
            i.check_in_out = check_in_out
    return info

@login_required()
def addToCartDetails(request, ref):
    html = None
    if request.method == 'POST':
        cart_param = request.POST.get("cart")
        hotel = get_object_or_404(Hotel, reference=ref)
        status = -1
        cart = Cart.objects.filter(Q(flag=1) & Q(pk=cart_param) & Q(hotel_id=hotel.pk) & Q(user_id=request.user.pk))
        if cart.exists():
            cart = cart.first()
            extra_person = Extra_person_rate.objects.filter(hotel_id=hotel.pk, active=1).exists()
            check_in_out = Check_in_out_rate.objects.filter(hotel_id=hotel.pk, active=1).exists()
            cart_detail = Cart_detail.objects.filter(cart_id=cart.pk, flag=1)
            if cart_detail.exists():
                for idx, c in enumerate(cart_detail.all()):
                    Guest.objects.filter(cart_detail_id=c.pk).update(flag=3)
                    obj_cart = Cart_detail.objects.get(pk=c.pk)
                    if check_in_out:
                        obj_cart.check_out_flag = request.POST.getlist('check_out_flag')[idx]
                        obj_cart.check_in_flag = request.POST.getlist('check_in_flag')[idx]
                    if extra_person:
                        obj_cart.extra_person_quantity = request.POST.getlist('extra_person_flag')[idx]
                    obj_cart.save()
                form = registerGuestFromReservationForm(request.POST)
                if form.is_valid():
                    for idx, c in enumerate(cart_detail.all()):
                        fullname = request.POST.getlist('fullname')[idx]
                        mobile = request.POST.getlist('mobile')[idx]
                        nationality = request.POST.getlist('nationality')[idx]
                        obj = Guest(room=c.room, cart_detail=c, fullname=fullname, mobile=mobile, nationality=nationality)
                        obj.save()
                        stepChangeStatus(cart.pk, 2)

                        status = 1
                        info = getInfoFromCart_(cart.pk , cart.hotel_id)
                        for i in info:
                            i.extra_person = extra_person
                            i.check_in_out = check_in_out

                        context = {
                            'info': info,
                            'form_pay': placeOrderForm,
                            'ref': hotel.reference,
                            'cart': cart,
                        }
                        html = render_to_string('cart/_reservation_payment_form.html',context=context, request=request)
                        # object = form.save(commit=False)
                        # object.room = c.room
                        # object.cart_detail = c
                        # object.save()
                else:
                    status = -1
            else:
                status = -1
        else:
            status = -1
    else:
        status = -1
    context = {
        'status': status,
        'html': html,
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


def confirmation(request, reference):
    context = {}
    return render(request, 'pages/confirmation.html', context)


def cart(request, ref):
    hotel = get_object_or_404(Hotel, reference=ref)
    if request.session.session_key or request.user.is_authenticated:
        session_key = request.session.session_key
        cart = Cart.objects.filter(flag=1, hotel_id=hotel.pk)
        if request.user.is_authenticated:
            cart = cart.filter(user_id=request.user.pk)
        else:
            cart = cart.filter(secure_key=session_key)
        if cart.exists():

            cart = cart.select_related('hotel__check_in_out_rate', 'hotel__breakfast_rate',
                                       'hotel__extra_person_rate').prefetch_related(Prefetch(
                'cart_detail',
                queryset=Cart_detail.objects.filter(flag=1).select_related('room',
                                                                           'room__default_cover').prefetch_related(
                    'room__room_facility_set', 'room__room_images_set', Prefetch(
                        'room__room_discount',
                        queryset=Discount.objects.filter(Q(active=1) & Q(start_date__lt=timezone.now()) & Q(
                            end_date__gt=timezone.now())).distinct())))).first()
        else:
            return redirect(reverse('hotelCategory'))
        for r in cart.cart_detail.all():
            diff = (cart.check_out - cart.check_in).days
            r.room.price = (diff * r.room.price) * r.quantity
        step = Step.objects.get(cart_id=cart.pk)
        info = None
        if step.step == 2:
            info = getInfoFromCart_(cart.pk , cart.hotel_id, True)
        context = {
            'info': info,
            'step': step,
            'ref': ref,
            'cart': cart,
            'form': registerUserFromReservationForm,
            'form_1': registerGuestFromReservationForm,
            'form_pay': placeOrderForm
        }
        return render(request, 'pages/cart.html', context)
    else:
        return redirect(reverse('hotelCategory'))


def addToCart(request, ref):
    if request.method == 'POST':
        if not request.session.session_key:
            request.session.save()
        session_key = request.session.session_key
        hotel = get_object_or_404(Hotel, reference=ref)
        if request.user.is_authenticated:
            cart_check = Cart.objects.filter(user_id=request.user.pk, hotel_id=hotel.pk,flag=1)
        else:
            cart_check = Cart.objects.filter(secure_key=session_key, hotel_id=hotel.pk,flag=1)

        checkIn = int(request.POST.get('check-in')) / 1000
        checkOut = int(request.POST.get('check-out')) / 1000
        checkInDate = datetime.datetime.fromtimestamp(float(checkIn))
        checkOutDate = datetime.datetime.fromtimestamp(float(checkOut))
        checkIn = datetime.datetime.fromtimestamp(checkIn)
        checkOut = datetime.datetime.fromtimestamp(checkOut)
        diff = (checkOut - checkIn).days
        if diff > 0:
            if not cart_check.exists():
                if request.user.is_authenticated:
                    cart_check = Cart(hotel_id=hotel.pk, check_in=checkInDate, check_out=checkOutDate,
                                      user_id=request.user.pk, secure_key=session_key)
                else:
                    cart_check = Cart(hotel_id=hotel.pk, check_in=checkInDate, check_out=checkOutDate,
                                      secure_key=session_key)
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
                                stepChangeStatus(cart_check.pk, 1)
                                flag = True
                if flag:
                    return redirect(reverse('cart', kwargs={'ref': ref}))

        return redirect(reverse('hotelPage', kwargs={'ref': ref,'title': hotel.name})+'?diff=false')

def stepChangeStatus(cart_id, step):
    obj_step = Step.objects.filter(cart_id=cart_id)
    if obj_step.exists():
        obj_step.update(step=step)
    else:
        step = Step(cart_id=cart_id, step=step)
        step.save()


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

def calcOrderInfo(cart):
    total_discount = 0
    total_products = cart.cart_detail.all().count()
    total_price = 0
    extra_person_rate = 0
    check_in_out_rate = 0
    nights = (cart.check_out - cart.check_in).days
    if cart.extra_person:
        extra_person_rate = cart.hotel.extra_person_rate.rate
    if cart.check_in_out:
        check_in_out_rate = cart.hotel.check_in_out_rate.rate
    for detail in cart.cart_detail.all():
        extra_person_quantity = detail.extra_person_quantity
        check_in_flag = detail.check_in_flag
        check_out_flag = detail.check_out_flag
        if detail.room.room_discount.all().count() > 0:
            first = detail.room.room_discount.all()[0]
            if first.reduction_type == 2:
                price = detail.room.price - first.reduction
                total_discount += price
            elif first.reduction_type == 1:
                price = ((100 - first.reduction) / 100) * detail.room.price
                total_discount += price
            else:
                price = detail.room.price
        else:
            price = detail.room.price
        total_price += nights * price
        total_price *= detail.quantity
        if check_in_flag == 1:
            total_price += check_in_out_rate
        if check_out_flag == 1:
            total_price += check_in_out_rate
        if extra_person_quantity > 0:
            total_price += extra_person_rate * extra_person_quantity
    context = {
        'total_discount' : total_discount,
        'total_products' : total_products,
        'total_price' : total_price,
    }
    return context
@login_required()
def placeOrders(request, ref, cart_id):
    hotel = get_object_or_404(Hotel, reference=ref)
    url = None
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = placeOrderForm(request.POST)
            if form.is_valid():
                cart_exists = Cart.objects.filter(user_id=request.user.pk, hotel_id=hotel.pk, pk=cart_id, flag=1)
                cart_obj = cart_exists.first()
                cart_obj.extra_person = Extra_person_rate.objects.filter(hotel_id=hotel.pk, active=1).exists()
                cart_obj.check_in_out = Check_in_out_rate.objects.filter(hotel_id=hotel.pk, active=1).exists()
                if cart_exists.exists():
                    info = calcOrderInfo(cart_obj)
                    order_obj = form.save(commit=False)
                    order_obj.user = cart_obj.user
                    order_obj.cart = cart_obj
                    order_obj.hotel = cart_obj.hotel
                    order_obj.total_discount = info['total_discount']
                    order_obj.total_amount = info['total_price']
                    order_obj.total_products = info['total_products']
                    order_obj.reference = str(uuid.uuid1())[:7]
                    order_obj.save()
                    stepChangeStatus(cart_obj.pk, 3)
                    cart_exists.update(flag=2)
                    url = reverse('confirmation', kwargs={'reference': order_obj.reference}),
                    status = 1
                else:
                    status = 0
            else:
                #print(form.errors.as_data())
                status = -1

            context = {
                "url": url,
                "status": status,
            }
            return JsonResponse(context)