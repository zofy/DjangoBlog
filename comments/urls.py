from django.conf.urls import url
from comments.views import IndexView, ShowView

app_name = 'comments'

urlpatterns = [
    url(r'^(?P<blog_id>[0-9]+)/comments/(?P<page>[0-9]+)/$', IndexView.as_view(), name='index'),
    # url(r'^1/comments/0/$', IndexView.as_view(), name='index'),
    url(r'^comments/(?P<id>[0-9]+)/$', ShowView.as_view(), name='show'),
]
