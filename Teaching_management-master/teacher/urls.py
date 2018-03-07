from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^teacher_courses/(.+)/$', views.course, name='teacher_courses'),
    url(r'^teacher_hw/(.+)/$', views.hw, name='teacher_hw'),
    url(r'^new_hw/(.+)/$', views.new_hw, name='new_hw'),
    url(r'^mark_hw/(.+)/$', views.mark_hw, name='mark_hw'),
    url(r'^teacher_forum/(.+)/$', views.teacher_forum, name='teacher_forum'),
    url(r'^teacher_resource_comment/(.+)/$',
        views.teacher_resource_comment, name='teacher_resource_comment'),
    url(r'^message/(.+)/$', views.message, name='teacher_message'),
    url(r'^add_ta/(.+)/$', views.addta, name='add_ta'),
    url(r'^teacher_forum$', views.teacher_forum, name='forum'),
    url(r'^logout$', views.logout, name='logout'),
]
