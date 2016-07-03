from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Blog
from blog.serializers import BlogSerializer


def home(request):
    return HttpResponseRedirect('/blogs')


def new(request):
    return render(request, 'blog/new.html')


def edit(request, id):
    try:
        blog = Blog.objects.get(pk=id)
    except:
        return Http404
    return render(request, 'blog/edit.html', {'blog': blog})


class IndexView(APIView):
    def get(self, request):
        posts = Blog.objects.all()
        serializer = BlogSerializer(posts, many=True)
        return Response({'blogs': serializer.data}, template_name='blog/index.html')

    def post(self, request):
        data = {atr: request.data[atr] for atr in request.data}
        Blog.objects.create_post(data)
        return HttpResponseRedirect('/blogs')


class ShowView(APIView):

    def get(self, request, **kwargs):
        # return render(request, 'blog/show.html', {'blog': Blog.objects.get_blog(id)})
        return Response({'blog': BlogSerializer(self.get_blog(kwargs['id'])).data}, template_name='blog/show.html')

    def put(self, request, *args):
        # post = Blog.objects.get_blog(id)
        # data = {atr: request.data[atr] for atr in request.data}
        # for atr in data:
        #     setattr(post, atr, data[atr])
        # post.save()
        Blog.objects.update_post(args[0])
        return HttpResponseRedirect(reverse('blog:show', args=[id]))

    def delete(self, request, *args):
        Blog.objects.delete_post(args[0])
        # Blog.objects.get_blog(id).delete()
        return HttpResponseRedirect('/blogs')
