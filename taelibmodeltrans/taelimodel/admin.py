from django.contrib import admin
from .models import *
# Register your models here.
from modeltranslation.translator import register, TranslationOptions
# # from .models import books

@register(books)
class BookTranslationOptions(TranslationOptions):
     fields = ('bookname', 'bookdiscrib')  # Specify the fields you want to translate


@register(catagory)
class catagorytranslationoptions(TranslationOptions):
    fields=('catagoryname',)

admin.site.register(catagory)
admin.site.register(books)
admin.site.register(cart)
admin.site.register(Language)
admin.site.register(file)
admin.site.register(Adminstration)
admin.site.register(Projects)

# admin.site.register(books,bookAdmin)

# @admin.register(books)
# class BookAdmin(TranslationAdmin):
#     pass