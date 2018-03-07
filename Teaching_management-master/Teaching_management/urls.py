"""Teaching_management URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    url(r'^$', views.login),
    url(r'^login', views.login),
    url(r'^register', views.register),
    url(r'^student/', include('student.urls')),
    url(r'^ta/', include('ta.urls')),
    url(r'^teacher/', include('teacher.urls')),
    url(r'^administrator/', include('administrator.urls')),
    url(r'^visitor/', include('visitor.urls')),
    url(r'^admin', admin.site.urls),
    path('admin/', admin.site.urls),
]
