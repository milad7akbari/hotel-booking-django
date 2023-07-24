from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from apps.blog.models import Main


# Create your views here.
def blogMainPage(request, category_id=None):
    # fake = Faker()
    # for i in range(1, 30):
    #     c = Category(pk=i, title=fake.text(), desc=fake.paragraphs(nb=1), active=1)
    #     c.save()
    #
    #     for b in range(1, 30):
    #         v = Main(category_blog_id=i, title=fake.text(), desc=fake.paragraphs(nb=1), active=1)
    #         v.save()

    if category_id is not None:
        blogs = Main.objects.filter(active=1, category_blog_id=category_id).select_related('default_image').values(
            'pk',
            'title',
            'desc',
            'date_upd',
            'default_image__file')
    else:
        blogs = Main.objects.filter(active=1).select_related('default_image').values(
            'pk',
            'title',
            'desc',
            'date_upd',
            'default_image__file')
    p = Paginator(blogs, 5)
    page_number = request.GET.get('page')

    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)

    context = {
        'blogs': page_obj,
    }
    return render(request, 'blog/home.html', context)


# Create your views here.

def blogPage(request, pk, title):
    blog = Main.objects.filter(active=1, pk=pk).values('pk', 'title', 'desc').first()
    context = {
        'blog' : blog
    }
    return render(request, 'blog/blog_page.html', context)
