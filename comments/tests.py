from random import choice, randint

from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase, APIRequestFactory
from comments.models import Comment
from comments.views import ShowView


class CommentTestCase(APITestCase):
    factory = APIRequestFactory()

    @staticmethod
    def generate_comments(num):
        comments = [CommentTestCase.create_comment()]
        for __ in range(num - 1):
            idx = randint(0, int(2 * len(comments)))
            c = CommentTestCase.create_comment()
            if idx < len(comments):
                parent = comments[idx]
                c.depth = parent.depth + 1
                c.path = parent.path + ' ' + str(c.id)
            c.save()
            comments.append(c)

    def test_sorting(self):
        self.generate_comments(10000)
        self.assertEquals(Comment.objects.count(), 10000)
        Comment.objects.all().order_by('path')
        # for c in Comment.objects.all():
        #     print(c.path)
        # print('************')
        # for c in Comment.objects.all().order_by('path'):
        #     print(c.path)

    @staticmethod
    def create_comment(blog_id=1, body='some text', depth=1):
        c = Comment.objects.create(blog_id=blog_id, body=body, depth=depth)
        c.path = str(c.id)
        c.save()
        return c
        # return Comment.objects.create(blog_id=blog_id, body=body, depth=depth)

    def test_create_comment(self):
        data = {'blog_id': 8, 'body': 'generated text', 'depth': 2}
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
        data = {'depth': 3, 'body': 'Some random updated text', 'up_votes': 1, 'down_votes': 1}
        view = ShowView.as_view()
        response = view(self.factory.put(url, data), c.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.get().depth, data['depth'])
        self.assertEqual(Comment.objects.get().body, data['body'])
        self.assertEqual(Comment.objects.get().up_votes, 1)
        self.assertEqual(Comment.objects.get().down_votes, 1)
        self.assertNotEquals(Comment.objects.get().lower_bound, 0)

    def test_show_delete(self):
        c = self.create_comment()
        self.assertEqual(Comment.objects.count(), 1)
        url = reverse('comments:show', args=[c.id])
        view = ShowView.as_view()
        response = view(self.factory.delete(url), c.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 0)
