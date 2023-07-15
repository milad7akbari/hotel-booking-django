from django.db.models import Count

from apps.blog.models import Category, Main
from apps.front.models import Cart


def header(request):
    context = {}
    if 'blog/' in request.get_full_path():
        header_category = Category.objects.filter(active=1, flag=1).order_by('-date_add')[:4]
        category = Category.objects.filter(active=1, flag=0).annotate(count_blogs=Count('main')).values('pk', 'title', 'desc', 'count_blogs').order_by('?')[:10]
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
    elif 'cart/' in request.get_full_path():
        ref = None
        cart = Cart.objects.select_related('hotel').filter(flag=1)
        if request.user.is_authenticated:
            cart = cart.filter(user_id=request.user.pk)
        else:
            if request.session.session_key:
                session_key = request.session.session_key
                cart = cart.filter(secure_key=session_key)
        if cart.exists():
            cart = cart.first()
            ref = cart.hotel.reference
        context = {
            'ref': ref,
        }
    return context
