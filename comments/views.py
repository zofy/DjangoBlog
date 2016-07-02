from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from comments.models import Comment
from comments.serializers import CommentSerializer

COMMENTS_PER_PAGE = 5


class IndexView(APIView):
    def get(self, request, **kwargs):
        comments = Comment.objects.get_blog_comments(kwargs['blog_id'])[
                   int(kwargs['page']) * COMMENTS_PER_PAGE: (int(kwargs['page']) + 1) + COMMENTS_PER_PAGE]
        serializer = CommentSerializer(comments, many=True)
        return Response({'comment_tree': serializer.data}, template_name='comments/index.html')

    def post(self, request, **kwargs):
        # in data must be id of a parent_comment
        data = {atr: request.data[atr] for atr in request.data}
        Comment.objects.create_comment(kwargs['blog_id'], data)
        return HttpResponseRedirect('/blogs')


class ShowView(APIView):
    def get(self, request, **kwargs):
        # return render(request, 'comments/show.html', {'comments': Comment.objects.get_comment(id)})
        # return Response({'comment': CommentSerializer(self.get_comment(id)).data}, template_name='comments/show.html')
        return Response(CommentSerializer(Comment.objects.get_comment(kwargs['id'])).data)

    def put(self, request, **kwargs):
        data = {atr: request.data[atr] for atr in request.data}
        Comment.objects.update_comment(kwargs['id'], data)
        return HttpResponseRedirect(reverse('comments:show', args=[kwargs['id']]))

    def delete(self, request, *args):
        Comment.objects.delete_comment(args[0])
        return HttpResponseRedirect('/blogs')
