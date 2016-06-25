from django.conf.urls import url

from .views import IndexView, ShowView
from . import views

app_name = 'blog'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^blogs/$', IndexView.as_view(), name='index'),
    url(r'^blogs/(?P<id>[0-9]+)/$', ShowView.as_view(), name='show'),
    url(r'^blogs/(?P<id>[0-9]+)/edit/$', views.edit, name='edit'),
    url(r'^blogs/new/$', views.new, name='new'),
]
