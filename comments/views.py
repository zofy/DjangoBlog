from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from rest_framework.views import APIView

from comments.models import Comment


class IndexView(APIView):
    def get_comments(self, id):
        try:
            return Comment.objects.filter(parent=id)
        except:
            return Http404

    def get(self, request, id):
        comments = self.get_comments(id)
        return render(request, 'comments/index.html', {'comments': comments})
        # serializer = BlogSerializer(posts, many=True)
        # return Response(serializer.data)

    def post(self, request):
        data = {atr: request.data[atr] for atr in request.data}
        Comment.objects.create(**data).save()
        return HttpResponseRedirect('/comments')


class ShowView(APIView):
    def get_comments(self, id):
        try:
            return Comment.objects.filter(parent=id)
        except:
            return Http404

    def get(self, request, id):
        return render(request, 'comments/show.html', {'comments': self.get_comments(id)})
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