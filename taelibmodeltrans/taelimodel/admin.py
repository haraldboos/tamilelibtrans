from django.contrib import admin
from .models import *
# Register your models here.
from modeltranslation.admin import TranslationAdmin

from modeltranslation.translator import register, TranslationOptions
# # from .models import books

@register(books)
class BookTranslationOptions(TranslationOptions):
     fields = ('bookname', 'bookdiscrib')  # Specify the fields you want to translate

@register(Adminstration)
class AdminastrationTransulation(TranslationOptions):
    fields=('ocation',)

@register(catagory)
class catagorytranslationoptions(TranslationOptions):
    fields=('catagoryname',)
@register(BannerQuote)
class BannerQuoteAdmin(TranslationOptions):
    fields= ('quote', )
@admin.register(catagory)
class CategoryAdmin(TranslationAdmin):
    list_display = ('catagoryname', 'showstatus', 'createdate')

# admin.site.register(books)
@admin.register(books)
class BookAdmin(TranslationAdmin):
    list_display = ('bookno', 'bookname', 'status', 'uploadedtime', 'bookpageno', 'bookprize', 'paid')
    search_fields = ('bookname',)
    list_filter = ('status', 'paid', 'uploadedtime')

# @admin.register(cart)
@admin.register(cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('orderid', 'user', 'bookno', 'ordertime', 'booklang', 'orderstatus')
    search_fields = ('orderid', 'user__username', 'bookno__bookname')
    list_filter = ('orderstatus', 'ordertime')


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('get_bookno', 'get_booknamecatagory', 'get_bookname','booklang',)
    search_fields = ('bookno__bookname','bookno__bookno')
    list_filter = ('booklang',)
    def get_bookname(self, obj):
        return obj.bookno.bookname
    def get_bookno(self, obj):
        return obj.bookno.bookno
    def get_booknamecatagory(self, obj):
        return obj.bookno.catgryname .catagoryname
    get_bookname.short_description = 'Book Name'
    get_booknamecatagory.short_description='Catagory'
# admin.site.register(file)
@admin.register(Adminstration)

class AdministrationAdmin(admin.ModelAdmin):
    list_display = ('adid', 'name', 'ocation')
    search_fields = ('name',)


@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('prid', 'name', 'date')
    search_fields = ('name',)
    list_filter = ('date',)

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'status')
    list_filter = ('status', 'date')
@admin.register(BannerQuote)
class BannerQuoteAdmin(TranslationAdmin):
    list_display = ('quote', 'date', 'status')
    search_fields = ('quote',)
    list_filter = ('status', 'date')
@admin.register(Oursponser)
class OursponserAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'status')
    search_fields = ('name',)
    list_filter = ('status', 'date')


# admin.site.register(books,bookAdmin)

# @admin.register(books)
# class BookAdmin(TranslationAdmin):
#     pass