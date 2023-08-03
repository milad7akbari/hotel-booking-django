from django.db.models import Count, Q
from apps.base.models import Cities, Footer, Meta
from apps.blog.models import Category, Main
from apps.front.models import Cart, Cart_detail, Step


def header(request):
    context = {}
    if 'blog/' in request.get_full_path():
        header_category = Category.objects.filter(active=1, flag=1).order_by('-date_add')[:4]
        category = Category.objects.filter(active=1, flag=0).annotate(count_blogs=Count('main')).values('pk', 'title',
                                                                                                        'desc',
                                                                                                        'count_blogs').order_by(
            '?')[:10]
        blogs_related = Main.objects.filter(active=1).select_related('default_image').values(
            'pk',
            'title',
            'desc',
            'date_upd',
            'default_image__file').order_by('?')[:7]
        context = {
            'blogs_related': blogs_related,
            'header_category': header_category,
            'category': category,
        }
    elif 'admin/' not in request.get_full_path():
        session_key = None
        check_in = None
        ref = None
        check_out = None
        step = 1
        if request.user.is_authenticated or request.session.session_key:
            if request.session.session_key:
                session_key = request.session.session_key
            cart = Cart_detail.objects.select_related('cart').filter(Q(flag=1) & (Q(cart__user_id=request.user.pk) | Q(cart__secure_key=session_key)))
            if cart.exists():
                cart = cart.last()
                cart = Cart.objects.select_related('hotel').filter(pk=cart.cart_id,flag=1).first()
                if cart is not None:
                    step = Step.objects.get(cart_id=cart.pk)
                    ref = cart.hotel.reference
                    check_in = cart.check_in
                    check_out = cart.check_out
            else:
                ref = None
        else:
            ref = None
        context = {
            'step': step,
            'ref': ref,
            'check_in': check_in,
            'check_out': check_out,
        }


    return context


def footer(request):
    city = Cities.objects.filter(hotel__isnull=False).annotate(count=Count('name')).all()[:10]
    footer = Footer.objects.all()
    postal_code = 0
    phone = 0
    email = 0
    instagram = 0
    whatsapp = 0
    telegram = 0
    for i in footer:
        if i.name == 'postal_code':
            postal_code = i.value
        if i.name == 'phone':
            phone = i.value
        if i.name == 'email':
            email = i.value
        if i.name == 'instagram':
            instagram = i.value
        if i.name == 'whatsapp':
            whatsapp = i.value
        if i.name == 'telegram':
            telegram = i.value
    context = {
        'phone': phone,
        'email': email,
        'instagram': instagram,
        'whatsapp': whatsapp,
        'telegram': telegram,
        'postal_code': postal_code,
        'city': city,
        'footer': footer,
    }
    return context
