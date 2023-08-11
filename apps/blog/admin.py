from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from modeltranslation.admin import TranslationAdmin
from .models import Main, Files, Category


class FilesAdmin(TranslationAdmin):
    model = Files
    list_filter = ('active',)
    list_display = ('pk', 'file', 'title', 'note', 'active', 'date_add')


class CategoryAdmin(TranslationAdmin):
    model = Category
    list_filter = ('active',)
    list_display = ('pk', 'title', 'desc', 'flag', 'active', 'date_add')


class MainAdmin(SummernoteModelAdmin, TranslationAdmin):
    model = Main
    list_select_related = ('category_blog' , 'default_image')
    list_filter = ('active',)
    list_display = ('pk', 'category_blog', 'default_image', 'title', 'active', 'date_add')
    summernote_fields = ('desc',)
    # creating admin class

    def category_blog(self, obj):
        return obj.category_blog.title

    def default_image(self, obj):
        return obj.default_image.title


admin.site.register(Category, CategoryAdmin)
admin.site.register(Files, FilesAdmin)
admin.site.register(Main, MainAdmin)
