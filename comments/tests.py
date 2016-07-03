from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase, APIRequestFactory
from comments.models import Comment
from comments.views import ShowView


class CommentTestCase(APITestCase):
    factory = APIRequestFactory()

    def create_comment(self, blog_id=1, body='some text', depth=1):
        return Comment.objects.create(blog_id=blog_id, body=body, depth=depth)

    def test_create_comment(self):
        data = {'blog_id': 8, 'body': 'generated text', 'depth': 2 }
        url = reverse('comments:index', args=[8, 0])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().blog_id, 8)

    def test_show_comments(self):
        c = self.create_comment()
        url = reverse('comments:index', args=[c.blog_id, 0])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()['comment_tree'][0]['body'], 'some text')

    def test_show_get(self):
        c = self.create_comment()
        url = reverse('comments:show', args=[c.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['blog_id'], c.blog_id)

    def test_show_put(self):
        c = self.create_comment()
        url = reverse('comments:show', args=[c.id])
        data = {'depth': 3, 'body': 'Some random updated text', 'up_votes': 1}
        view = ShowView.as_view()
        response = view(self.factory.put(url, data), c.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.get().depth, data['depth'])
        self.assertEqual(Comment.objects.get().body, data['body'])
        self.assertEqual(Comment.objects.get().up_votes, 1)
        self.assertNotEquals(Comment.objects.get().lower_bound, 0)

    def test_show_delete(self):
        c = self.create_comment()
        self.assertEqual(Comment.objects.count(), 1)
        url = reverse('comments:show', args=[c.id])
        view = ShowView.as_view()
        response = view(self.factory.delete(url), c.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 0)