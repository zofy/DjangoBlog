from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from blog.models import Blog
from blog.views import ShowView


class BlogTestCase(APITestCase):
    factory = APIRequestFactory()

    @staticmethod
    def create_post(title='Post1', body='Some text'):
        return Blog.objects.create(title=title, body=body)

    def test_create_post(self):
        data = {'title': 'TestTitle'}
        url = reverse('blog:index')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Blog.objects.count(), 1)
        self.assertEqual(Blog.objects.get().title, data['title'])

    def test_index(self):
        self.create_post()
        url = reverse('blog:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()['blogs'][0]['title'], 'Post1')

    def test_show_get(self):
        b = self.create_post()
        url = reverse('blog:show', args=[b.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # print response.json()
        self.assertEqual(response.json()['blog']['title'], 'Post1')

    def test_show_put(self):
        b = self.create_post()
        url = reverse('blog:show', args=[b.id])
        data = {'title': 'Updated title', 'body': 'Some random updated text'}
        view = ShowView.as_view()
        response = view(self.factory.put(url, data), b.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Blog.objects.get().title, data['title'])
        self.assertEqual(Blog.objects.get().body, data['body'])

    def test_show_delete(self):
        b = self.create_post()
        self.assertEqual(Blog.objects.count(), 1)
        url = reverse('blog:show', args=[b.id])
        view = ShowView.as_view()
        response = view(self.factory.delete(url), b.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Blog.objects.count(), 0)



