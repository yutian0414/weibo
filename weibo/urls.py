"""weibo URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from weibo_app1 import views as app1_views
from django.conf.urls import include
from django.contrib.auth.views import login
from django.conf.urls.static import static
from weibo.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',app1_views.index),
    url(r'^sign_up/$',app1_views.sign_up),
    url(r'^home/([^/]{1,20})/([^/]{0,100})/$', app1_views.home),
    url(r'^sign_in/',app1_views.sign_in),
    url(r'^chart_with_rescently/$',app1_views.chart_with_rescently),
]
urlpatterns+=static('/media/',document_root=MEDIA_ROOT)