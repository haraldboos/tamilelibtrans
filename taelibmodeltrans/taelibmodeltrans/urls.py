"""taelibmodeltrans URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.conf.urls import handler500

from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from taelimodel.views import StripeWeb_Hook
handler500='taelimodel.views.custom_500'
urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    # path('rosetta/', include('rosetta.urls')),
    path('roseta/', include('rosetta.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('accounts/', include('allauth.urls')),
    path('', include('taelimodel.urls')),
)
urlpatterns += [
    path('webhook/', StripeWeb_Hook.as_view(), name='stripe-webhook'),
]
# urlpatterns =[
#     path('admin/', admin.site.urls),
#     # path('rosetta/', include('rosetta.urls')),
#     path('roseta/', include('rosetta.urls')),

#     path('', include('taelimodel.urls')),
# ]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)