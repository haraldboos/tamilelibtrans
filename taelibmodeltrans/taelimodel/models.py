from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from gdstorage.storage import GoogleDriveStorage, GoogleDrivePermissionType, GoogleDrivePermissionRole, GoogleDriveFilePermission

# from django.utils.translation import gettext_lazy a
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
    catagoryname = models.CharField(max_length=50,null=False,blank=False,verbose_name="Enter Catagory Name")
    showstatus  = models.BooleanField(default=False,help_text="0-show,1-Hide",verbose_name="Hide")
    createdate = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.catagoryname
    class Meta:
        verbose_name = 'Books Catagory'
        verbose_name_plural = 'Books Catagory'

class books(models.Model):
   
    bookname = models.CharField(max_length=40,verbose_name="Enter Book Name")
    bookdiscrib = models.CharField(max_length=1000,null=False,blank = False,verbose_name="Discribe Book")



    catgryname = models.ForeignKey(catagory,on_delete=models.CASCADE,verbose_name="Select Catagory Name",related_name='category') 
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
    paid=models.BooleanField(default=True,verbose_name="book paid")

    def save(self, *args, **kwargs):
      
        if not self.bookno:
            self.bookno = books.objects.count() + 1
        
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Book No:{self.bookno} Book Name '{self.bookname}'  "

 
    # def save(self, *args, **kwargs):
    #     if not self.bookid:
    #         self.bookid = bookidget()
    #     super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Books '
        verbose_name_plural = 'Books'

# @register(books)
  

# register(books,booktr)    
class cart(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="Ordered User")
    bookno=models.ForeignKey(books,on_delete=models.CASCADE,verbose_name="Booke Number")
    orderid=models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    ordertime=models.DateTimeField(auto_now_add=True,verbose_name="Ordered Time")
    booklang=models.CharField(null=False,verbose_name="Selected book languageg ",default=None,max_length=10)
    bookpr=models.IntegerField(default=None)
    orderstatus=models.BooleanField(default=0,help_text="0-payment not done,1-payment done")
    
    
    def save(self, *args, **kwargs):
        if not self.orderid:
            self.orderid = uuid.uuid4()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.orderid)
    class Meta:
        verbose_name = 'Book Order In Cart'
        verbose_name_plural = 'Book Order In Cart'
class Language(models.Model):
    # permission = GoogleDriveFilePermission(
    # GoogleDrivePermissionRole.READER,
    # GoogleDrivePermissionType.ANYONE,
    
    # )
    # permission = {
    #         'role':'reader',
    #         'type':'anyone',
    #         'capabilities':{
    #             'canDownload': False
    #         }
    #     }
    fiestorg= GoogleDriveStorage()

    Language_choices=(
            ('Tamil','Tamil'),
            ('English','English'),
            ('German','German'),
            ('Italy','Italy'),
            ('French','French')
            
    )
    bookno = models.ForeignKey(books,on_delete=models.CASCADE,verbose_name="Book Number")
    booklang = models.CharField(null=False,choices=Language_choices,blank=False,default=None,max_length=8,verbose_name="File Language")
    bookpdf = models.FileField(upload_to=uploadbook,null=False,blank=False,verbose_name="Book selected Language")
    gdbookid =models.CharField(max_length=255,blank=True,verbose_name="the id for every file from google drive")
    # paid=models.BooleanField(default=False,verbose_name="Paid Book or")
    def uploadtogoogle(self):
        print(self.bookpdf)
        tamilpucredintial=service_account.Credentials.from_service_account_file('taelimodel/tamilpubliclib.json')
        sex = build('drive','v3',credentials=tamilpucredintial)
        bok = f"{self.bookno}_{self.booklang}"
        print(bok)
        fmesex={
            'name':bok,
            'parents':['1f7Szb1WwH0ROe25HyEdp7ruq7zTOhuyC']
        }
        miyaboobs=MediaFileUpload(self.bookpdf.path,resumable=True)
        room = sex.files().create(body=fmesex, media_body=miyaboobs).execute()
        filepath = self.bookpdf
        # print(filepath)
        # fid = self.fiestorg._get_file_id(filepath)

        self.gdbookid=room.get('id')
        # print(self.gdbookid)
        permission = {
            'type':'anyone',
            'role':'reader',
            'allowFileDiscovery':False,    
            'copyContent': False,
            'viewersCanCopyContent': False, 
            'canShare': False


            
        }
        sex.permissions().create(fileId=self.gdbookid, body=permission).execute()
        
    def save(self, *args, **kwargs):
        #     self.uploadtogoogle()

        #     print(self.gdbookid)
        #     super().save(*args, **kwargs)
        # # self.uploadtogoogle()
        #     if self.gdbookid is None:
        #         print("Google Drive file ID is None, cannot assign to gdbookid.")
        if not self.pk: 
            # print('11') # Check if the instance is being created
            super().save(*args, **kwargs)  # Call save to generate the primary key

        self.uploadtogoogle()  # Upload the file to Google Drive
        # print('12')
    # Now that the file has been uploaded, save the instance with the gdbookid
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('bookno', 'booklang')
        verbose_name = 'Books In Languages'
        verbose_name_plural = 'Books In Languages'
         
    def __str__(self):
        return f"{self.bookno} in {self.booklang} "

# fiestorg= GoogleDriveStorage(permissions=(permission,))
class file(models.Model):
    pass
#     permission = GoogleDriveFilePermission(
#     GoogleDrivePermissionRole.READER,
#     GoogleDrivePermissionType.ANYONE,
#     # capabilities={'canDownload':False}
# )
#     # fiestorg= GoogleDriveStorage(permissions=[permission])

#     file_id=models.CharField(max_length=20,null=False,blank=False,default=None)
#     file=models.FileField(upload_to='mypt', storage=fiestorg)
#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
class Adminstration(models.Model):
    name = models.CharField(max_length=30,null=False,default=None,verbose_name='Person Name')
    image=models.ImageField(upload_to=uploadcover,null=False,blank=False,default=None,verbose_name="Profile Picture")
    adid =models.AutoField(primary_key=True,editable=False)
    ocation=models.CharField(max_length=20,null=False,default=None,verbose_name="Ocation")
    status=models.BooleanField(default=True)

    class Meta:
        # unique_together = ('bookno', 'booklang')
        verbose_name = 'Our Adminastraion'
        verbose_name_plural = 'Our Adminastraion'

class Projects(models.Model):
    prid =models.AutoField(primary_key=True,editable=False)
    name = models.CharField(max_length=20,null=False,default=None,verbose_name="Project Name")
    date = models.DateField(verbose_name="Project Date")
    cover=models.ImageField(upload_to=uploadcover,null=False,blank=False,default=None,verbose_name="Project Cover")
    file=models.FileField(upload_to=uploadbook,null=False,blank=False,default=None,verbose_name="Project File")
    status=models.BooleanField(default=True)
    class Meta:
        # unique_together = ('bookno', 'booklang')
        verbose_name = 'Our Projects'
        verbose_name_plural = 'Our Projects'
class Banner(models.Model):
    date=models.DateTimeField(auto_now=True)
    image=models.ImageField(upload_to=uploadbook,verbose_name="upload A Home Banner")
    status=models.BooleanField(default=True)
    # quote=models.CharField(max_length=40,verbose_name="quote",blank=True)

    # def __str__(self):
    #     return f"Banner {self.id} - {self.quote}"
    class Meta:
        # unique_together = ('bookno', 'booklang')
        verbose_name = 'Home Banner'
        verbose_name_plural = 'Home Banner'
class Oursponser(models.Model):
    logo=models.ImageField(upload_to=uploadbook,verbose_name="Sponser'd Logo",default=None)
    name=models.CharField(max_length=20,verbose_name="Sponsord Name",default=None)
    date=models.DateTimeField(auto_now=True)
    status=models.BooleanField(default=True)
    class Meta:
        # unique_together = ('bookno', 'booklang')
        verbose_name = 'Our Sponser'
        verbose_name_plural = 'Our Sponser'
class BannerQuote(models.Model):
    quote=models.CharField(max_length=60,default=None,verbose_name="Quote")
    date=models.DateTimeField(auto_now=True)
    status=models.BooleanField(default=True)

    class Meta:
        # unique_together = ('bookno', 'booklang')
        verbose_name = 'Banner Quote'
        verbose_name_plural = 'Banner Quote'

