from datetime import datetime
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=30)
    honor = models.PositiveIntegerField(default=0)


class BlogManager(models.Manager):
    def get_blog(self, id):
        try:
            return Blog.objects.get(id=id)
        except:
            raise Exception('Blog not found!')

    def create_post(self, data):
        Blog.objects.create(**data).save()

    def update_post(self, id):
        pass

    def delete_post(self, id):
        pass


class Blog(models.Model):
    title = models.CharField(max_length=100)
    image = models.URLField(
        default="http://www.theblogstarter.com/wp-content/uploads/2016/01/start-your-blog-4-steps.png")
    body = models.TextField()
    created = models.DateField(default=datetime.now())
    authors = models.ManyToManyField(Author)
    hidden = models.BooleanField(default=False)

    objects = BlogManager()
