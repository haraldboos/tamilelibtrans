from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name="home"),
    path('coll',views.collection,name="coll"),
    path('login',views.login_pg,name="login"),
    path('logout',views.logout_pg,name="logout"),
    path('register',views.register,name="register"),
    path('cart',views.mycart,name="cart"),
    path('search',views.bsearch_view,name='bsearch'),
    path('myaccount',views.uacunt,name="acount"),
    path('viewcart/<uuid:orderid>',views.rmcart,name="removecart"),
    path('viewcart',views.cartpage,name="viewcart"),
    path('cprodect/<str:name>',views.cprodects,name="cprodect"),
    path('switch/<str:language>/', views.swlanguage, name='swlanguage'),

    path('cprodect/<str:name>/<str:prodect>',views.inspectpro,name="inspectpro"),
    path('vpdf/<int:bookno>/<str:booklang>',views.pdfviws,name='vpdf'),

]