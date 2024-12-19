from django.shortcuts import render
# Create your views here.
from django.db.models import Q
import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.urls import reverse
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
import stripe.error
import stripe.webhook
from .form import userform ,SearchForm
from .models import *
from django.utils.translation import activate,get_language
from django.views import View
from django.contrib.auth import authenticate,login,logout
from django.conf import settings
import stripe
from django.views.decorators.csrf import csrf_exempt


stripe.api_key = settings.STRIPE_SECRET_KEY


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
    # print(request.path)
    if request.method == 'POST':
        # print(x=x+1)
        # print(request)
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
                # print(cart.objects.filter(user=request.user.id,bookno__bookno=bookno,booklang=booklanguage,orderstatus=0).exists())
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
    return render(request,'elibt/teams.html',{'times':ad})



def ourproject(request):
    project=Projects.objects.filter(status=True)
    # fffk=range(9)
    # for l in project:
    #     print(l.cover.url,'ll')
    return render(request,'elibt/ourpoject.html',{'times':project,})
    # if request.user.is_authenticated:
    #     pdff=Projects.objects.filter(prid=pid)
    #     # print(pdff)
    #     # for y in pdff:
    #     #     print(y.name)
    #         # for e in y:
    #         #     print(e)
    #     if not pdff:
    #         return render(request, 'elibt/projectview.html', {'error_message': 'The project not uploaded yet.'})
    #     return render(request,'elibt/projectview.html',{'pddf':pdff,})
    # else:
    #    messages.warning(request,"You Must Have to login to view the Projects")
    #    return redirect("/login")
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



# stripe.api_key = settings.STRIPE_SECRET_KEY

def payment_view(request):
    if request.method == "POST":
        try:
            # Create a payment intent
            intent = stripe.PaymentIntent.create(
                amount=5000,  # Amount in cents (e.g., $50)
                currency='usd',
                payment_method=request.POST['payment_method_id'],
                confirmation_method='manual',
                confirm=True,
            )
            return JsonResponse({'success': True, 'payment_intent': intent})
        except stripe.error.CardError as e:
            return JsonResponse({'error': str(e)}, status=400)

    return render(request, 'elibt/payments.html', {
        'publishable_key': settings.STRIPE_PUBLIC_KEY
    })
@csrf_exempt
def cheackout(request):
    cartd=cart.objects.filter(user=request.user.id,orderstatus=False)
    # print(vars(cartd))
    return render(request,'elibt/cheackout.html',{'cart':cartd,'pub_key': settings.STRIPE_PUBLIC_KEY})

def payment_sucess_page(request):
    return render(request,'elibt/suecss_payment.html')
def payment_error_page(request):
    return render(request,'elibt/payment_error.html')

class Stripepaymentgateway(View):
    """
    stripe payment gatye way 
    """

    def post(self,request):
       
        cartbooks= cart.objects.filter(user=request.user.id,orderstatus=False)
    #    data = request
        line_items = []
        cartids=[str(cart_id) for cart_id in cartbooks]
        totalAmount=0
        for product in cartbooks:
            # print(p)
            # print(product.orderid)
            # cartids.append(product.orderid)

            line_items.append({
                    'price_data': {
                        'currency': 'chf',  # Replace with your currency code
                        'product_data': {
                            'name': f"{product.bookno.bookname} ({product.booklang})",
                            'description':product.bookno.bookdiscrib,
                            'images':[request.build_absolute_uri(product.bookno.bookcover.url)]

                        },
                        'unit_amount': int(product.bookpr * 100),  # Stripe expects amounts in cents
                    },
                    'quantity': 1,
                })
        stripe.api_key=settings.STRIPE_SECRET_KEY
        success_url = request.build_absolute_uri(reverse('sucesspage'))
        cancel_url = request.build_absolute_uri(reverse('eror_payment_page'))

        session=stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={
                'cart_ids':json.dumps(cartids),
            }


        )
        # print(session)

        for books in cartbooks:
            books.payment_intent_id = session.payment_intent
            books.save()
        return JsonResponse({'sessionId': session.id})

        #    print(products.booklang)
    #    print(data)
    #    HttpResponse()
# @csrf_exempt
@method_decorator(csrf_exempt, name='dispatch')
class StripeWeb_Hook(View):
    """
    stripe web hook
"""
    # @method_decorator(csrf_exempt, name='dispatch')
  
    # @csrf_exempt
    def post(self,request, *args, **kwargs):
        # print(request.body)
        # payload=request.body    
        payload=request.body
        event=None
        sig_header=request.META['HTTP_STRIPE_SIGNATURE']
        try:
            event=stripe.Webhook.construct_event(
                payload,sig_header,settings.STRIPE_ENDPOINT_SECRET
            )
        except ValueError as e:
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            return HttpResponse(status=400)
        # return JsonResponse({'messages':'wehook'},status=200)
        if event['type']=='checkout.session.completed':
            session=event['data']['object']
            print(session)
            # print(event['type'])
            # print(event['type'])
        return HttpResponse(status=200)
    # print("webhook")
        # sig_header = request.META
        # print("webhook")
        # event=None
        # try:
        #     print(sig_header)
        #     event= stripe.Webhook.construct_event(
        #         payload,sig_header,settings.STRIP_WEBHOOK_SECREAT
        #     )
        # except ValueError as e:
        #     # Invalid payload
        #     return HttpResponse(status=400)
        # except stripe.error.SignatureVerificationError as e:
        #     return HttpResponse(status=400)
        # if event['type']=='checkout.session.completed':
        #     print(event)
        #     session = event['data']