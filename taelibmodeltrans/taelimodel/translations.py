from modeltranslation.translator import register, TranslationOptions
from .models import books,catagory,Banner,BannerQuote

@register(books)
class BookTranslationOptions(TranslationOptions):
    fields = ('bookname', 'bookdiscrib')  # Specify the fields you want to translate

@register(catagory)
class catagorytranslationoptions(TranslationOptions):
    fields=('catagoryname',)

@register(BannerQuote)
class bannerQuotetranslationoptions(TranslationOptions):
    fields = ('quote',)