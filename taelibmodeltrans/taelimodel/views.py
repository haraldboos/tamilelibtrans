from django.shortcuts import render

# Create your views here.

import json
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .form import userform ,SearchForm
from .models import *
from django.utils.translation import activate,get_language

from django.contrib.auth import authenticate,login,logout

# Create your views here.
none = "nothing"
def home(request):
    # collection= catagory.objects.filter(showstatus=0)
    # ,{"list":collection}
    bd = Language.objects.all()
    print(request.LANGUAGE_CODE)
    return render(request,"elibt/hm.html",{"bd":bd})
def collection(request):

    collection= catagory.objects.filter(showstatus=0)
    
    return render(request,"elibt/coll.html",{"list":collection})

def swlanguage(request, language):
    print(language)
    activate(language)
    # pass
    cur_lang=get_language()
    print(cur_lang)
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
        print(request)
        uf=userform(request.POST)
        if uf.is_valid():
            uf.save()
            messages.success(request,"Registration Sucess You Can Login Now ...! ")
            return redirect('/login')

    # return HttpResponse("<h1>register</h1>")
    return render(request,"elibt/register.html",{'form':uf})

def cprodects(request,name):
    print(request.LANGUAGE_CODE)
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
        if cart.objects.filter(user=request.user,orderstatus=0):
            upboks= cart.objects.filter(user=request.user,orderstatus=0)
            print(upboks)
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
        bklang=Language.objects.filter(bookno=bkno)
        
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
                print(fk)
                print(request)
                booklanguage=fk['booklang']
                # bookname=fk['bknam']
                bookno=fk['bookno']
                prize = fk['prize']
                userid = request.user.id
                username=request.user
                print(bookno,prize)
                print(userid)
                print(username)
                
                book_status = books.objects.get(bookno=bookno)
                if book_status:
                    if cart.objects.filter(user=request.user.id,bookno=bookno,booklang=booklanguage):
                        print("books alredy in  cart")
                        messages.warning(request,"books alredy in  cart")
                        return JsonResponse({'status':'product alredy in cart'})
                    else:
                        cart.objects.create(user=username,bookno=book_status,booklang=booklanguage,bookpr=prize)
                        messages.warning(request,"books add cart sucess fully in  cart")
                        return JsonResponse({'status':'proudct add cart sucess'},status=200)
                else:
                    messages.warning(request,"books not avilable yet comming soon ")
                    return JsonResponse({'status':'product alredy in cart'})


                    


            else:
                messages.warning(request,"You Must Have to login to add cart")
                return JsonResponse({'status':'login to add cart'}, status=200)
    else:
        return JsonResponse({'status':'invalid Access'}, status=200)
    # return HttpResponse("<h1>this is cart</h1>")

def pdfviws(request,bookno,booklang):
    if request.user.is_authenticated:
        if cart.objects.filter(user=request.user,bookno=bookno,booklang=booklang,orderstatus=0).exists():
            print('yes is there')
            book=Language.objects.get(bookno=bookno,booklang=booklang)
            # bk=Language.objects.get(bookno=2,booklang='Tamil')
            print(book)
            # print(bk.bookpdf,bk)


            return render(request,"elibt/fk/user/acbook.html",{'book':book})

        
        else :
            errro='You are restricted to this book'
            return HttpResponse('<h1>omm</h1>')
    else :  
            
            messages.warning(request,"You Must Have to login to view the book")

            return HttpResponse('<h1>omm</h1>')
    

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
def ourteam(request):
    pass
def webhook(request):
    print(request)