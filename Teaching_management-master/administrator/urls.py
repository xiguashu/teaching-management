from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^administrator_courses/(.+)/$',views.courses, name='courses'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^liuyan',views.liuyan),
    url(r'^deleteliuyan/(.+)/$',views.deleteliuyan)
]
