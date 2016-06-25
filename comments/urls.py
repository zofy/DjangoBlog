from django.conf.urls import url
from comments.views import IndexView, ShowView

app_name = 'comments'

urlpatterns = [
    url(r'^(?P<id_blog>[0-9]+)/comments/$', IndexView.as_view(), name='index'),
    url(r'^(?P<id_blog>[0-9]+)/comments/(?P<id>[0-9]+)/$', ShowView.as_view(), name='show'),
]
