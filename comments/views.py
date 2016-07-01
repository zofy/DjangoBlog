from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from comments.models import Comment
from comments.serializers import CommentSerializer

COMMENTS_PER_PAGE = 5


class IndexView(APIView):
    def get(self, request, blog_id, page):
        # comments = Comment.objects.get_blog_comments(blog_id)
        comments = Comment.objects.get_blog_comments(blog_id)[int(page) * COMMENTS_PER_PAGE: (int(page) + 1) + COMMENTS_PER_PAGE]
        # return render(request, 'comments/index.html', {'comment_tree': comments})
        serializer = CommentSerializer(comments, many=True)
        return Response({'comment_tree': serializer.data}, template_name='comments/index.html')

    def post(self, request, blog_id):
        # in data must be id of a parent_comment
        data = {atr: request.data[atr] for atr in request.data}
        Comment.objects.create_comment(blog_id, data)
        return HttpResponseRedirect('/blogs')


class ShowView(APIView):
    def get(self, request, id):
        return render(request, 'comments/show.html', {'comments': Comment.objects.get_comment(id)})
        # return Response(CommentSerializer(self.get_comment(id)).data)

    def put(self, request, id):
        data = {atr: request.data[atr] for atr in request.data}
        Comment.objects.update_comment(id, data)
        return HttpResponseRedirect(reverse('comments:show', args=[id]))

    def delete(self, request, id):
        Comment.objects.delete_comment(id)
        return HttpResponseRedirect('/blogs')
