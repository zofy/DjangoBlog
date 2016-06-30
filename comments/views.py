from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from comments.models import Comment
from comments.serializers import CommentSerializer


class IndexView(APIView):

    def get(self, request, blog_id):
        comments = Comment.objects.get_comments(blog_id)
        return render(request, 'comments/index.html', {'comment_tree': comments})
        # serializer = CommentSerializer(comments, many=True)
        # return Response(serializer.data)

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