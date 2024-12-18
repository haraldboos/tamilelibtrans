from django.urls import path,re_path
# from django.conf.urls.i18n import i18n_patterns
from . import views
urlpatterns=[
    path('',views.home,name="home"),
    path('coll/',views.collection,name="coll"),
    path('login/',views.login_pg,name="login"),
    path('logout/',views.logout_pg,name="logout"),
    path('register/',views.register,name="register"),
    path('cart/',views.mycart,name="cart"),
    path('search/',views.bsearch_view,name='bsearch'),
    path('myaccount/',views.uacunt,name="acount"),
    path('viewcart/<uuid:orderid>/',views.rmcart,name="removecart"),
    path('viewcart/',views.cartpage,name="viewcart"),
    path('cprodect/<str:name>/',views.cprodects,name="cprodect"),
    path('switch/<str:language>/', views.swlanguage, name='swlanguage'),
    # path('webhook/',views.StripeWeb_Hook.as_view(),name='webhook'),
    path('cprodect/<str:name>/<str:prodect>/',views.inspectpro,name="inspectpro"),
    path('vpdf/<int:bookno>/<str:booklang>/',views.pdfviws,name='vpdf'),
    path('ourteams/',views.ourteams,name='teams'),
    path('ourproject/',views.ourproject,name='project'),
    path('ourproject/<str:pid>/',views.projectv,name='ppview'),

# path('paytest/',views.paymenttesting)
    path('payment/', views.payment_view, name='payment'),
    path('cheackout/',views.cheackout,name='cheackout'),
    re_path('^sucess/$',views.payment_sucess_page,name='sucesspage'),
    path('error/',views.payment_error_page,name='eror_payment_page'),

    path('pay/',views.Stripepaymentgateway.as_view(),name='stripay'),
]
# urlpatterns = [
#     *i18n_patterns(*urlpatterns,prefix_default_language=False),
#     pa
# ]