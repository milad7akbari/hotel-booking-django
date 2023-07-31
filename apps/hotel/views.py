from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Min, Count, Q, Prefetch
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.base.models import Cities
from apps.hotel.forms import reviewsForm
from apps.hotel.models import Hotel, Facility, Close_spots, Images, Room, Room_images, Reviews, Discount


def hotelCategory(request):
    city_param = request.GET.get("city")
    facility_param = request.GET.get("facility")
    filter_param = request.GET.get("filter")
    search_param = request.GET.get("search")
    sorting_param = request.GET.get("sorting")
    sort = 'name'
    if sorting_param is not None:
        if sorting_param == 'name-asc':
            sort = 'name'
        elif sorting_param == 'name-desc':
            sort = '-name'
        elif sorting_param == 'star-asc':
            sort = 'stars'
        elif sorting_param == 'star-desc':
            sort = '-stars'
    hotel = Hotel.objects.filter(active=1, room__price__isnull=False, room__active__exact=1).select_related(
        'default_cover', 'city').prefetch_related('facility_set' , Prefetch(
                'room_set',
                queryset=Room.objects.filter(
                    Q(active=1))
            ) , Prefetch(
                'hotel_discount',
                queryset=Discount.objects.filter(
                    Q(active=1) & Q(start_date__lt=timezone.now()) & Q(end_date__gt=timezone.now()))
            )).annotate(count_reviews=Count('reviews', distinct=True, filter=Q(reviews__active=1))).order_by(sort)


    if city_param is not None or facility_param is not None or search_param is not None:
        if city_param is not None:
            city_param = tuple([str(i) for i in city_param.split(",")])
            hotel = hotel.filter(city__name__in=city_param).order_by(sort)
        if facility_param is not None:
            facility_param = tuple([str(i) for i in facility_param.split(",")])
            hotel = hotel.filter(facility__title__in=facility_param).order_by(sort)
        if search_param is not None:
            hotel = hotel.filter(Q(name__contains=search_param) | Q(city__name__contains=search_param)).order_by(sort)
    if sorting_param == 'price-desc':
        sort_price = '-price'
    else:
        sort_price = 'price'
    for i in hotel:
        discount = i.hotel_discount.first()
        price = i.room_set.order_by(sort_price).first().price
        if discount is not None:
            reduction_type = discount.reduction_type
            reduction = discount.reduction
            i.reduction = discount.reduction
            i.reduction_type = reduction_type
            i.price_bef = price
            if reduction_type == 2:
                i.price = price - reduction
            if reduction_type == 1:
                i.price = ((100 - reduction) / 100) * price
        else:
            i.price = price
    p = Paginator(hotel, 5)
    page_number = request.GET.get('page')

    try:
        hotel = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        hotel = p.page(1)
    except EmptyPage:
        hotel = p.page(p.num_pages)

    if filter_param is not None:
        context = {
            'hotel': hotel,
        }
        html = render_to_string('hotel/_list_hotels.html', context)
        return JsonResponse(html, safe=False)
    else:
        city = Cities.objects.filter(hotel__isnull=False).annotate(count=Count('name')).all()
        facility = Facility.objects.filter(active=1, hotel__isnull=False).all()
        context = {
            'hotel': hotel,
            'city': city,
            'facility': facility,
        }
        return render(request, 'hotel/home.html', context)


# Discount.objects.filter(active=True, start_date__lt=datetime.datetime.now() , end_date__gt=datetime.datetime.now()).values('reduction')
def hotelPage(request, ref, title):
    diff = request.GET.get('diff')
    hotel = Hotel.objects.filter(active=1, reference=ref).select_related('default_cover', 'city').prefetch_related(Prefetch(
                'hotel_discount',
                queryset=Discount.objects.filter(
                    Q(active=1) & Q(start_date__lt=timezone.now()) & Q(end_date__gt=timezone.now()))
            )).first()
    if hotel is not None:
        room = Room.objects.filter(active=1, hotel_id=hotel.pk).select_related('default_cover').prefetch_related(
            'room_images_set',Prefetch(
                'hotel__hotel_discount',
                queryset=Discount.objects.filter(
                    Q(active=1) & Q(start_date__lt=timezone.now()) & Q(end_date__gt=timezone.now()))
            ),
            'room_facility_set')
        facility = Facility.objects.filter(hotel_id=hotel.pk, active=1).all()
        close_spots = Close_spots.objects.filter(hotel_id=hotel.pk, active=1).all()
        reviews = Reviews.objects.filter(hotel_id=hotel.pk, active=1).values('title', 'desc_good', 'desc_bad',
                                                                             'short_desc',
                                                                             'reviews_reply__short_desc', 'stars',
                                                                             'user__first_name', 'user__last_name',
                                                                             'date_add')
        for i in room:
            discount = i.hotel.hotel_discount.first()
            price = i.price
            if discount is not None:
                reduction_type = discount.reduction_type
                reduction = discount.reduction
                i.reduction = discount.reduction
                i.reduction_type = reduction_type
                i.price_bef = price
                if reduction_type == 2:
                    i.price = price - reduction
                if reduction_type == 1:
                    i.price = ((100 - reduction) / 100) * price
            else:
                i.price = price
        context = {
            'diff': diff,
            'form': reviewsForm,
            'reviews': reviews,
            'room': room,
            'close_spots': close_spots,
            'hotel': hotel,
            'facility': facility,
        }
        return render(request, 'hotel/hotel_page.html', context)


def reviewsSubmit(request):
    if request.method == 'POST':
        user = request.user
        form = reviewsForm(request.POST, user)
        if form.is_valid():
            form.save()
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


def imagesHotel(request, ref):
    get = request.GET.get("get")
    if get is not None:
        if get == 'l':
            data = get_object_or_404(Hotel, reference=ref)
            images = Images.objects.filter(hotel_id=data.pk, active=1).all()
        elif get == 'r':
            data = get_object_or_404(Room, pk=ref)
            images = Room_images.objects.filter(room=data.pk, active=1).all()
        else:
            return HttpResponseNotFound()
        context = {
            'images': images,
        }
        return render(request, '_partial/_images.html', context)
    else:
        return None


def getHotels(request):
    hotel = Hotel.objects.filter(active=1, room__price__isnull=False, room__active__exact=1).select_related(
        'default_cover', 'city').prefetch_related('facility_set').annotate(
        min_room_price=Min('room__price')).all()
    context = {
        'hotel': hotel,
    }
    city = request.GET.get("city")
    facility = request.GET.get("facility")
    html = render_to_string('hotel/_list_hotels.html', context)
    return JsonResponse(html, safe=False)
