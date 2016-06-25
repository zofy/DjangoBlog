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
        return render(request, 'blog/index.html', {'blogs': posts})
        # serializer = BlogSerializer(posts, many=True)
        # return Response(serializer.data)

    def post(self, request):
        data = {atr: request.data[atr] for atr in request.data}
        Blog.objects.create(**data).save()
        return HttpResponseRedirect('/blogs')


class ShowView(APIView):
    def get_blog(self, id):
        try:
            return Blog.objects.get(pk=id)
        except:
            return Http404

    def get(self, request, id):
        return render(request, 'blog/show.html', {'blog': self.get_blog(id)})
        # return Response(BlogSerializer(self.get_blog(id)).data)

    def put(self, request, id):
        post = self.get_blog(id)
        data = {atr: request.data[atr] for atr in request.data}
        for atr in data:
            setattr(post, atr, data[atr])
        post.save()
        return HttpResponseRedirect(reverse('blog:show', args=[id]))

    def delete(self, request, id):
        self.get_blog(id).delete()
        return HttpResponseRedirect('/blogs')
