from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from comments.models import Comment, CommentManager
from comments.serializers import CommentSerializer


class IndexView(APIView):

    def get(self, request, blog_id):
        comments = CommentManager.get_comments(blog_id)
        return render(request, 'comments/index.html', {'comment_tree': comments})
        # serializer = CommentSerializer(comments, many=True)
        # return Response(serializer.data)

    def post(self, request, blog_id):
        # in data must be id of a parent_comment
        data = {atr: request.data[atr] for atr in request.data}
        if data['parent']:
            parent_comment = self.get_parent_comment(data['parent'])
            data['blog_id'] = parent_comment.blog_id
            data['path'] = parent_comment.path
        else:
            data['blog_id'] = blog_id
        c = Comment.objects.create(**data).save()
        c.path += ' ' + c.id
        c.save()
        return HttpResponseRedirect('/blogs')


class ShowView(APIView):
    def get_comment(self, id):
        try:
            return Comment.objects.get(id=id)
        except:
            return Http404

    def get(self, request, id):
        return render(request, 'comments/show.html', {'comments': self.get_comment(id)})
        # return Response(CommentSerializer(self.get_comment(id)).data)

    def put(self, request, id):
        comment = self.get_comment(id)
        data = {atr: request.data[atr] for atr in request.data}
        for atr in data:
            setattr(comment, atr, data[atr])
        comment.save()
        return HttpResponseRedirect(reverse('comments:show', args=[id]))

    def delete(self, request, id):
        self.get_comment(id).delete()
        return HttpResponseRedirect('/blogs')