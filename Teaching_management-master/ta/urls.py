from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ta_courses', views.course, name='ta_courses'),
    url(r'^ta_hw', views.hw, name='ta_hw'),
    url(r'^new_hw', views.new_hw, name='new_hw'),
    url(r'^mark_hw', views.mark_hw, name='mark_hw'),
    url(r'^ta_forum', views.ta_forum, name='ta_forum'),
    url(r'^ta_resource_comment', views.ta_resource_comment, name='ta_resource_comment'),
    url(r'^message', views.message, name='ta_message'),
]
