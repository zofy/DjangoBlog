from django.db import models


class CommentManager(models.Manager):

    def get_comment(self, id):
        try:
            return Comment.objects.get(id=id)
        except:
            raise Exception('Comment not found!')

    def get_blog_comments(self, blog_id):
        try:
            return Comment.objects.filter(blog_id=blog_id).order_by('path')
        except:
            return []

    def get_parent_comment(self, parent_id):
        try:
            return Comment.objects.get(id=parent_id)
        except:
            raise Exception('Parent comment not found!')

    def create_comment(self, blog_id, data):
        if 'parent' in data:
            parent_comment = self.get_parent_comment(data['parent'])
            data['path'] = parent_comment.path
        data['blog_id'] = blog_id
        c = Comment.objects.create(**data)
        c.save()
        if c.path:
            c.path += ' ' + str(c.id)
        else:
            c.path = str(c.id)
        c.save()

    def update_comment(self, id, data):
        comment = self.get_comment(id)
        for atr in data:
            setattr(comment, atr, data[atr])
        comment.save()

    def delete_comment(self, id):
        self.get_comment(id).delete()


class Comment(models.Model):
    body = models.TextField()
    up_votes = models.PositiveIntegerField(default=0)
    down_votes = models.PositiveIntegerField(default=0)
    _lower_bound = models.FloatField(default=0)
    depth = models.PositiveIntegerField(default=0)
    blog_id = models.PositiveIntegerField(default=0)  # id of Blog Post
    parent = models.PositiveIntegerField(default=None, null=True)
    path = models.TextField(default=None, null=True)
    hidden = models.BooleanField(default=False)

    objects = CommentManager()

    @property
    def lower_bound(self):
        return self._lower_bound

    # @lower_bound.setter
    # def lower_bound(self):
    #     self.set_lower_bound()

    def set_lower_bound(self):
        n = self.up_votes + self.down_votes
        if n == 0:
            return 0
        pos = self.up_votes
        z = 1.96
        phat = 1.0 * pos / n
        self.lower_bound = (phat + z * z / (2 * n) - z * ((phat * (1 - phat) + z * z / (4 * n)) / n)) / (
                                                                                                            1 + z * z / n) ** 0.5
