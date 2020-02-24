"""ermisAuth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from ermisPortal import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('index.html', views.index, name='index'),
    path('help.html', views.help, name='help'),
    path('contact.html', views.contact, name='contact'),
    path('workshop.html', views.workshop, name='workshop'),
    url(r'^$', views.index, name='index'),
    url(r'', include('mama_cas.urls')),
    url(r'^admin/', admin.site.urls),
    path('user/', include('dl_user.urls')),
    path('maps/cyprus.html', views.cyprus, name='cyprus'),
    path('maps/crete.html', views.crete, name='crete'),
    path('maps/lesvos.html', views.lesvos, name='lesvos'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]
