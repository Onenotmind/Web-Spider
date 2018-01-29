"""YeSpider URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from taobao.views import products
from django.views.static import serve
from taobao.views import search_pro
from taobao.views import index_init
from taobao.views import jd_product

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^index$', products),
    # url(r'^search$', products),
    url(r'^index/$', index_init),
    url(r'^search/$', products),
    # url(r'^js/$', jd_product),
    url(r'^staticfiles/(?P<path>.*)$',serve,{'document_root':settings.STATIC_ROOT}),

]
