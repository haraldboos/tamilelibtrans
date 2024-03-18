from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
# from modeltranslation.translator import TranslationOptions
# from modeltranslation.decorators import register
# from parler.models import TranslatableModel,TranslatedFields

import datetime
import os
import uuid

# Create your models here.
# @register
# class BookTranslationOptions(TranslationOptions):  # Rename the class for clarity
#     fields = ('bookname', 'bookdiscrib')  # Specify the fields to translate

# @register
# class CategoryTranslationOptions(TranslationOptions):
#     fields = ('catagoryname',)


def uploadcover(request,filename):
    curtime=datetime.datetime.now().strftime("%Y%m%d:%H%M%S")
    filenewname=curtime+filename
    return os.path.join('bookup/','bookcover/',filenewname)


def uploadbook(request,filename):
    getime = datetime.datetime.now().strftime("%Y%m%d:%H%M%S")
    filenewname = getime+filename
    return os.path.join('bookup/','book/',filenewname)


# @register
class catagory(models.Model):
    catagoryname = models.CharField(max_length=50,null=False,blank=False,verbose_name=_("Enter Catagory Name"))
    showstatus  = models.BooleanField(default=False,help_text="0-show,1-Hide",verbose_name=_("Status of The Book"))
    createdate = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.catagoryname

class books(models.Model):
   
    bookname = models.CharField(max_length=40,verbose_name=_("Enter Book Name"))
    bookdiscrib = models.CharField(max_length=1000,null=False,blank = False,verbose_name=_("Discribe Book"))



    catgryname = models.ForeignKey(catagory,on_delete=models.CASCADE,verbose_name=_("Select Catagory Name"),related_name=_('category')) 
    # bokid = bookidget()
    # bookname_fr=models.CharField()
    # bookname = models.CharField(max_length=40,verbose_name="Enter Book Name")
    bookcover = models.ImageField(upload_to=uploadcover,null=False,blank=False,verbose_name="Uploadbook Cover")
    # bookdiscrib = models.CharField(max_length=1000,null=False,blank = False,verbose_name="Discribe Book")
    status = models.BooleanField(default = 1,help_text="1-show,0-hide")
    uploadedtime = models.DateTimeField(auto_now_add=True)
    bookpageno =models.IntegerField(null=True,verbose_name="Enter book page")
    bookprize=models.IntegerField(default=None,verbose_name="Enter the prize of the book")
    bookno =models.IntegerField(editable=False,null=False,default=None,verbose_name="book no auto created")
    
    def save(self, *args, **kwargs):
      
        if not self.bookno:
            self.bookno = books.objects.count() + 1
        
        super().save(*args, **kwargs)
    def __str__(self):
        return str(self.bookno)
 
    # def save(self, *args, **kwargs):
    #     if not self.bookid:
    #         self.bookid = bookidget()
    #     super().save(*args, **kwargs)



# @register(books)
  

# register(books,booktr)    
class cart(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    bookno=models.ForeignKey(books,on_delete=models.CASCADE)
    orderid=models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    ordertime=models.DateTimeField(auto_now_add=True)
    booklang=models.CharField(null=False,verbose_name="book languageg u want",default=None,max_length=10)
    bookpr=models.IntegerField(default=None)
    orderstatus=models.BooleanField(default=0,help_text="0-payment not done,1-payment done")
    
    
    def save(self, *args, **kwargs):
        if not self.orderid:
            self.orderid = uuid.uuid4()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.orderid)

class Language(models.Model):
    Language_choices={
            'Tamil':'Tamil',
            'English':'English',
            'German':'German',
            'Italy':'Italy',
            'French':'French'
            
    }
    bookno = models.ForeignKey(books,on_delete=models.CASCADE)
    booklang = models.CharField(null=False,choices=Language_choices,blank=False,default=None,max_length=8,verbose_name="Enter The File Language")
    bookpdf = models.FileField(upload_to=uploadbook,null=False,blank=False,verbose_name="Upload In selected Language")

    class Meta:
        unique_together = ('bookno', 'booklang') 
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        return str(self.bookno)