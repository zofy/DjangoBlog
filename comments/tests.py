from random import choice, randint

import time
from django.core.urlresolvers import reverse
from django.db import transaction
from rest_framework.test import APITestCase, APIRequestFactory

from comments.context_manager import time_this
from comments.models import Comment
from comments.sorters import CommentSorter
from comments.updater import CommentUpdater
from comments.views import ShowView


class CommentTestCase(APITestCase):
    factory = APIRequestFactory()

    @staticmethod
    @transaction.atomic()
    def generate_comments(num):
        comments = [CommentTestCase.create_comment()]
        for __ in range(num - 1):
            idx = randint(0, int(1.2 * len(comments)))
            c = CommentTestCase.create_comment()
            if idx < len(comments):
                parent = comments[idx]
                c.depth = parent.depth + 1
                c.path = parent.path + ' ' + c.path
            c.save()
            comments.append(c)

    @staticmethod
    def create_comment(blog_id=1, body='some text', depth=0):
        c = Comment.objects.create(blog_id=blog_id, body=body, depth=depth)
        c.set_lower_bound()
        c.path = ' '.join([str(-c.lower_bound), str(c.id)])
        c.save()
        return c

    def test_sorting(self):
        self.generate_comments(10000)

        # self.assertEqual(Comment.objects.count(), 1000)
        # with time_this('Fetching'):
        comments = Comment.objects.get_blog_comments(1)
        with time_this('Updating'):
            comments[-1].up_votes = 1
        # comments[0].save()
        # CommentUpdater().update_line(comments[0], comments)
        # for c in comments:
        #     print(c.path + ': ' + str(c.depth))
        # print('*******************')
        # for c in Comment.objects.get_blog_comments(1):
        #     print(c.path + ': ' + str(c.depth))
        print(CommentSorter.check_sorted(Comment.objects.get_blog_comments(1)))

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
