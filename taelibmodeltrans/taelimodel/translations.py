from modeltranslation.translator import register, TranslationOptions
from .models import books

@register(books)
class BookTranslationOptions(TranslationOptions):
    fields = ('bookname', 'bookdiscrib')  # Specify the fields you want to translate
