from django.shortcuts import render

# Create your views here.
from django.db.models import Q

import json
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .form import userform ,SearchForm
from .models import *
from django.utils.translation import activate,get_language

from django.contrib.auth import authenticate,login,logout
import urllib.request
import hmac
import hashlib
import base64
import sys
from urllib.parse import urlencode, quote, quote_plus
from collections import OrderedDict
import requests


# Create your views here.
from django.shortcuts import render
def custom_400(request, exception):
    current_year = datetime.now().year
    return render(request, '400.html', {'current_year': current_year}, status=400)

def custom_404(request, exception):
    current_year = datetime.now().year
    return render(request, '404.html', {'current_year': current_year}, status=404)

def custom_500(request):
    current_year = datetime.now().year
    return render(request, '500.html', {'current_year': current_year}, status=500)
none = "nothing"
def home(request):

    # collection= catagory.objects.filter(showstatus=0)
    # ,{"list":collection}
    # messages.info(request, 'This is an info message.')
    # messages.success(request, 'Your account was successfully created!')
    # messages.warning(request, 'Your subscription is about to expire!')
    # messages.error(request, 'There was an error processing your payment.')

    abanner=Banner.objects.filter(status=True).order_by('-date')[0:5]
    bd = Language.objects.all()
    # print(request.LANGUAGE_CODE)
    spon=Oursponser.objects.filter(status=True)

    return render(request,"elibt/hm.html",{"bd":bd,"banner":abanner,"sponser":spon})
def collection(request):

    collection= catagory.objects.filter(showstatus=0)
    
    return render(request,"elibt/coll.html",{"list":collection})

def swlanguage(request, language):
    # print(language)
    activate(language)
    # pass
    cur_lang=get_language()
    # print(cur_lang)
    activate(language)
    return redirect("language","/")
    # print('oooma')
    # return redirect(request.META.get('HTTP_REFERER','/'))
def login_pg(request):
    if request.user.is_authenticated:
        return redirect("language","/")
    else:
        if request.method =='POST':
            
            uname = request.POST.get('username')
            pwd = request.POST.get('pass')
            userauth=authenticate(request,username=uname,password=pwd)
            if userauth is not None:
                login(request,userauth)
                messages.success(request,"Logged in Success")
                return redirect("/")
            else:
                messages.error(request,"Invalid User name or Password")
                return redirect("/login")

    # return HttpResponse("<h1>login</h1>")
    return render(request,"elibt/loginsite.html")

def logout_pg(request):
    # return HttpResponse("<h1>logout</h1>")
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged Out sucessfully")
    return redirect("/")

def register(request):
    uf=userform()
    if request.method=='POST':
        # print(request)
        uf=userform(request.POST)
        if uf.is_valid():
            uf.save()
            messages.success(request,"Registration Sucess You Can Login Now ...! ")
            return redirect('/login')

    # return HttpResponse("<h1>register</h1>")
    return render(request,"elibt/register.html",{'form':uf})

def cprodects(request,name):
    # print(request.LANGUAGE_CODE)
    activate(request.LANGUAGE_CODE)
    if catagory.objects.filter(catagoryname=name,showstatus=0):
        cbook =books.objects.filter(catgryname__catagoryname=name)
        return render(request,"elibt/cprodect.html",{"book":cbook})
    else:
        messages.warning(request,"not upload yet")
        non="No Uploads yet"
        return render(request,"elibt/cprodect.html",{"error":non})

def uacunt(request):
    if request.user.is_authenticated:
        # print(cart.objects.filter(user=request.user).filter(Q(orderstatus=True) | Q(bookno__paid=False)).exists())
        if cart.objects.filter(user=request.user).filter(Q(orderstatus=True) | Q(bookno__paid=False)).exists():
            upboks= cart.objects.filter(user=request.user).filter(Q(orderstatus=True) | Q(bookno__paid=False))
            # print(upboks)
            return render(request,"elibt/fk/user/mu.html", {'books':upboks})
        else:
            messages.warning(request,"ur account is empty buy any books")
            mss="ur account is empty.! buy any books"
            return render(request,"elibt/fk/user/mu.html", {'eupms':mss})

    else:
        return redirect('login')


    

def inspectpro(request,name,prodect):
    if catagory.objects.filter(catagoryname=name,showstatus=0):
        bk=books.objects.get(catgryname__catagoryname=name,bookname=prodect,status=1)
        bkno=bk.bookno
        bklang=Language.objects.filter(bookno__bookno=bkno)
       # print(bklang)
        return render(request,"elibt/prodins.html",{"book":bk,"booklang":bklang})
        
    else:
        messages.warning(request,"not upload yet")
        non="No Uploads yet"
        return render(request,"elibt/prodins.html",{"error":non})
    

def cartpage(request):
   
    if request.user.is_authenticated:
        car= cart.objects.filter(user=request.user)
        return render(request,"elibt/cart.html",{'cart':car})
    else:
            return redirect('login')
# def inspectpro(request, name, prodect):
#     try:
#         category = catagory.objects.get(catagoryname=name, showstatus=0)
#         book = books.objects.get(catgryname__catagoryname=name, bookname=prodect, status=1)
#         return render(request, "elibt/prodins.html", {"book": book})
#     except catagory.DoesNotExist:
#         messages.warning(request, "Category not found")
#     except books.DoesNotExist:
#         messages.warning(request, "Product not found")
    
#     return render(request, "elibt/prodins.html", {"error": "Category or Product not found"})
def rmcart(request,orderid):
    orid = cart.objects.get(orderid=orderid)
    orid.delete()
    return redirect('viewcart')
def mycart(request):

    x=0
    print(request.path)
    if request.method == 'POST':
        # print(x=x+1)
        print(request)
        if request.headers.get('x-requested-with')=='XMLHttpRequest':
            # print(request.data)
            # print(x=x+1)

            if request.user.is_authenticated:
                fk = json.loads(request.body.decode('utf-8'))
                # print(fk)
                # print(request)
                booklanguage=fk['booklang']
                # bookname=fk['bknam']
                bookno=fk['bookno']
                prize = fk['prize']
                userid = request.user.id
                username=request.user
                # print(bookno,prize)
                # print(userid)
                # print(username)
                
                book_status = books.objects.get(bookno=bookno)
                print(cart.objects.filter(user=request.user.id,bookno__bookno=bookno,booklang=booklanguage,orderstatus=0).exists())
                if book_status:
                    if cart.objects.filter(user=request.user.id,bookno__bookno=bookno,booklang=booklanguage,orderstatus=0).exists():
                        messages.warning(request,"books alredy in  cart")
                        return JsonResponse({'status':'books alredy in  cart'})
                    elif cart.objects.filter(user=request.user.id, bookno__bookno=bookno, booklang=booklanguage, orderstatus=1).exists():            
                        messages.warning(request, "You have already bought this book.")
                        return JsonResponse({'status': 'you already bought the book'})
                    else:
                        cart.objects.create(user=username, bookno=book_status, booklang=booklanguage, bookpr=prize)
                        messages.success(request, "Book added to cart successfully.")
                        return JsonResponse({'status':'proudct add cart sucess'},status=200)
                else:
                    messages.warning(request,"books not avilable yet comming soon ")
                    return JsonResponse({'status':'product not avalable yet'})

            else:
                messages.warning(request,"You Must Have to login to add cart")
                return JsonResponse({'status':'login to add cart'}, status=200)
    else:
        return JsonResponse({'status':'invalid Access'}, status=200)
    # return HttpResponse("<h1>this is cart</h1>")

def pdfviws(request,bookno,booklang):
    #print(booklang)
    if request.user.is_authenticated:
        if cart.objects.filter(user=request.user,bookno__bookno=bookno,booklang=booklang).filter(Q(orderstatus=True) | Q(bookno__paid=False)).exists():
            
            # print('yes is there')
            book=Language.objects.get(bookno__bookno=bookno,booklang=booklang)
            # bk=Language.objects.get(bookno=2,booklang='Tamil')
            # print(book)
            # print(bk.bookpdf,bk)


            return render(request,"elibt/fk/user/acbook.html",{'book':book})

        
        else :
            errro='You are restricted to this book'
            messages.warning(request,"You are restricted to this book")

            return HttpResponse('<h1>Youe are restricted</h1>')
    else :  
            
             messages.warning(request,"You Must Have to login to view the book")

             return redirect('/login')
    

def bsearch_view(request):
    reasultcat=False
    resultsbook=False
    non=False
    if request.method == 'POST':
        if request.POST.get('searchc',''):

            form = request.POST.get('searchc','')
            
            if books.objects.filter(bookname__icontains=form):
                resultsbook = books.objects.filter(bookname__icontains=form)  
                print(resultsbook)# Adjust field as per your model
                
                # return render(request, 'elibt/search.html', {'book': results, 'query': form})
            if catagory.objects.filter(catagoryname__icontains=form):
                # form = request.POST.get('searchc',''
                reasultcat=catagory.objects.filter(catagoryname__icontains=form)
                # print(form)
                # results = catagory.objects.filter(catagoryname__icontains=form)  
                print(reasultcat)# Adjust field as per your model
                
            if (reasultcat!=False or reasultcat!=False):   
                print('oooma') 
                return render(request, 'elibt/search.html', {'list': reasultcat, 'book': resultsbook,'form': form})
            # if form.is_valid():
            #     query = form.cleaned_data['query']
            #     results = books.objects.filter(bookname__icontains=query)  # Adjust field as per your model
            #  return render(request, 'search_results.html', {'results': results, 'query': query})
            else:
                non = 'no reasult for ur key word' 
                return render(request, 'elibt/search.html', {'form': form,'noon':non})

    else:
        non = 'no reasult for ur key word ', 
    return render(request, 'elibt/search.html', {'noon':non})

def csearch_view(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = catagory.objects.filter(title__icontains=query)  # Adjust field as per your model
            return render(request, 'search_results.html', {'results': results, 'query': query})
    else:
        form = SearchForm()
    return render(request, 'coll.html', {'form': form})
def payment(request,ammount,order):
    pass
def ourteams(request):
    fffk=range(9)
    ad=Adminstration.objects.filter(status=True)
    spon=Oursponser.objects.filter(status=True)
    return render(request,'elibt/teams.html',{'times':ad,'sponser':spon})
def webhook(request):
    print(request)
def ourproject(request):
    project=Projects.objects.filter(status=True)
    fffk=range(9)
    # for l in project:
    #     print(l.cover.url,'ll')
    return render(request,'elibt/ourpoject.html',{'times':project,})
    if request.user.is_authenticated:
        pdff=Projects.objects.filter(prid=pid)
        # print(pdff)
        # for y in pdff:
        #     print(y.name)
            # for e in y:
            #     print(e)
        if not pdff:
            return render(request, 'elibt/projectview.html', {'error_message': 'The project not uploaded yet.'})
        return render(request,'elibt/projectview.html',{'pddf':pdff,})
    else:
       messages.warning(request,"You Must Have to login to view the Projects")
       return redirect("/login")
def projectv(request,pid):
    if request.user.is_authenticated:
        pdff=Projects.objects.filter(prid=pid)
        # print(pdff)
        # for y in pdff:
        #     print(y.name)
            # for e in y:
            #     print(e)
        if not pdff:
            return render(request, 'elibt/projectview.html', {'error_message': 'The project not uploaded yet.'})
        return render(request,'elibt/projectview.html',{'pddf':pdff,})
    else:
       messages.warning(request,"You Must Have to login to view the Projects")
       return redirect("/login")


def paymenttesting(request):
   
    def generate_signature(query_string, api_secret):
        signature = hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256)
        return base64.b64encode(signature.digest()).decode('utf-8')

    def flatten_dict(dictionary, parent_key=''):
        flattened_data = {}
        for key, value in dictionary.items():
            new_key = f"{parent_key}[{key}]" if parent_key else key
            if isinstance(value, dict):
                flattened_data.update(flatten_dict(value, new_key))
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        flattened_data.update(flatten_dict(item, f"{new_key}[{i}]"))
                    else:
                        flattened_data[f"{new_key}[{i}]"] = item
            else:
                flattened_data[new_key] = value
        return flattened_data

    def encode_query_string(data):
        encoded_pairs = []
        for key, value in data.items():
            encoded_key = quote(key, safe='')
            if isinstance(value, list):
                for item in value:
                    encoded_pairs.append(f"{encoded_key}={quote(str(item), safe='')}")
            else:
                encoded_pairs.append(f"{encoded_key}={quote(str(value), safe='')}")
        return '&'.join(encoded_pairs)

    # Define the API endpoint and instance name
    api_endpoint = "https://api.zahls.ch/v1.0/Gateway/"
    instance_name = "tamilpubliclibrary.org"

    # Define the API secret
    api_secret = "uclUsfM1OxlJX2cDTH6iiRcbZVm6Bv"

    # Define the data payload using a normal dictionary
    raw_data = {
        'amount': 8925,
        'currency': 'CHF',
        'sku': 'P01122000',
        'pm': [
            'visa',
            'mastercard',
            'twint'
        ],
        'preAuthorization': 0,
        'reservation': 0,
        'referenceId': '975382',
        'fields': {
            'forename': {'value': 'Max'},
            'surname': {'value': 'Mustermann'},
            'email': {'value': 'max.mustermann@mysite.com'}
        },
        'successRedirectUrl': 'https://www.merchant-website.com/success',
        'failedRedirectUrl': 'https://www.merchant-website.com/failed',
        'basket': [
            {'name': 'Product', 'amount': 8000, 'quantity': 1, 'vatRate': 7.7},
            {'name': 'Shipping Costs', 'amount': 925, 'quantity': 1, 'vatRate': 0}
        ]
    }

    # Flatten the rawData
    data = flatten_dict(raw_data)

    # Create Query String
    query_string = urlencode(data, quote_via=quote_plus)

    # Generate the API Signature
    api_signature = generate_signature(query_string, api_secret)

    # Add the API signature to the data payload
    data['ApiSignature'] = api_signature

    # Generate QueryString for the Request
    request_query_string = encode_query_string(data)

    # Make the POST request
    response = requests.post(f"{api_endpoint}?instance={instance_name}", data=request_query_string)

    return HttpResponse(response.content)