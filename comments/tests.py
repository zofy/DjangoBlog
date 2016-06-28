from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from blog.tests import BlogTestCase
from comments.models import Comment
from comments.views import ShowView


class CommentTestCase(APITestCase):
    factory = APIRequestFactory()

    def create_comment(self, parent=1, body='some text', depth=1):
        return Comment.objects.create(parent=parent, body=body, depth=depth)

    def test_create_comment(self):
        data = {'parent': 8, 'body': 'generated text', 'depth': 2}
        url = reverse('comments:index', args=[8])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().parent, 8)

    def test_show_comments(self):
        c = self.create_comment()
        url = reverse('comments:index', args=[c.parent])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['body'], 'some text')

    def test_show_get(self):
        c = self.create_comment()
        url = reverse('comments:show', args=[c.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['parent'], c.parent)

    def test_show_put(self):
        c = self.create_comment()
        url = reverse('comments:show', args=[c.id])
        data = {'depth': 3, 'body': 'Some random updated text'}
        view = ShowView.as_view()
        response = view(self.factory.put(url, data), c.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.get().depth, data['depth'])
        self.assertEqual(Comment.objects.get().body, data['body'])

    def test_show_delete(self):
        c = self.create_comment()
        self.assertEqual(Comment.objects.count(), 1)
        url = reverse('comments:show', args=[c.id])
        view = ShowView.as_view()
        response = view(self.factory.delete(url), c.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 0)