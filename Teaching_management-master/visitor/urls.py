from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^visitor_courses', views.course, name='visitor_course'),
]