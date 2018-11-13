from __future__ import absolute_import


from django.conf.urls import url

from . import views
from django.views.generic import TemplateView

app_name = 'faces'

urlpatterns = [
    # url(r'^$', TemplateView.as_view(template_name="faces/home.html"), name='home'),
    url(r'^$', views.home, name='home'),

    url(r'^add/$', views.face_add, name='face_add'),
    url(r'^list/$', views.face_list, name='face_list'),
    url(r'^face/(?P<_id>[0-9]+)/$', views.face_detail, name='face_detail'),
    url(r'^face/delete/(?P<_id>[0-9]+)/$', views.face_delete, name='face_delete'),

    url(r'^clean/$', views.clean, name='clean'),

    url(r'^find/$', views.find, name='find'),
    url(r'^misc/$', views.misc, name='misc'),
]
