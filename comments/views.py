from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from comments.models import Comment
from comments.serializers import CommentSerializer

COMMENTS_PER_PAGE = 5


class IndexView(APIView):
    @staticmethod
    def get_comments(blog_id, sort_by):
        if sort_by is None:
            return Comment.objects.best_comments(blog_id)
        elif sort_by == 'newest':
            return Comment.objects.newest_comments(blog_id)
        elif sort_by == 'oldest':
            return Comment.objects.oldest_comments(blog_id)

    def get(self, request, **kwargs):
        comments = self.get_comments(request.data.get('sort_by'))[
                   int(kwargs['page']) * COMMENTS_PER_PAGE: (int(kwargs['page']) + 1) * COMMENTS_PER_PAGE]
        serializer = CommentSerializer(comments, many=True)
        return Response({'comment_tree': serializer.data}, template_name='comments/index.html')

    def post(self, request, **kwargs):
        # in data must be id of a parent_comment
        data = {atr: request.data[atr] for atr in request.data}
        Comment.objects.create_comment(kwargs['blog_id'], data)
        return HttpResponseRedirect('/' + kwargs['blog_id'] + '/' + 'comments/' + kwargs['page'] + '/')


class ShowView(APIView):
    def get(self, request, **kwargs):
        return Response(CommentSerializer(Comment.objects.get_comment(kwargs['id'])).data)

    def put(self, request, *args, **kwargs):
        data = {atr: request.data[atr] for atr in request.data}
        Comment.objects.update_comment(kwargs['id'], data)
        # Comment.objects.update_comment(args[0], data)
        return JsonResponse({'up': Comment.objects.get_comment(kwargs['id']).up_votes,
                             'down': Comment.objects.get_comment(kwargs['id']).down_votes,
                             'lb': Comment.objects.get_comment(kwargs['id']).lower_bound,
                             'path': Comment.objects.get_comment(kwargs['id']).path})

    def delete(self, request, *args, **kwargs):
        # Comment.objects.delete_comment(kwargs['id'])
        Comment.objects.delete_comment(args[0])
        return HttpResponseRedirect('/blogs')
