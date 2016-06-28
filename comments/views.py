from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from rest_framework.views import APIView

from comments.models import Comment


class IndexView(APIView):
    def get_comments(self, blog_id):
        try:
            return Comment.objects.filter(parent=blog_id)
        except:
            return Http404

    def get(self, request, blog_id):
        comments = self.get_comments(blog_id)
        return render(request, 'comments/index.html', {'comments': comments})
        # serializer = BlogSerializer(posts, many=True)
        # return Response(serializer.data)

    def post(self, request):
        data = {atr: request.data[atr] for atr in request.data}
        Comment.objects.create(**data).save()
        return HttpResponseRedirect('/blogs')


class ShowView(APIView):
    def get_comment(self, id):
        try:
            return Comment.objects.get(id=id)
        except:
            return Http404

    def get(self, request, id):
        return render(request, 'comments/show.html', {'comments': self.get_comment(id)})
        # return Response(BlogSerializer(self.get_blog(id)).data)

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