from django.db import transaction
from django.db import models

from comments.updater import CommentUpdater


class CommentManager(models.Manager):
    def get_comment(self, id):
        try:
            return Comment.objects.get(id=id)
        except:
            raise Exception('Comment not found!')

    def get_blog_comments(self, blog_id):
        try:
            return sorted(Comment.objects.filter(blog_id=blog_id), key=lambda c: [float(n) for n in c.path.split()])
        except:
            return []

    def get_parent_comment(self, parent_id):
        try:
            return Comment.objects.get(id=parent_id)
        except:
            raise Exception('Parent comment not found!')

    @transaction.atomic()
    def create_comment(self, blog_id, data):
        if 'parent' in data:
            parent_comment = self.get_parent_comment(data['parent'])
            data['path'] = parent_comment.path
            data['depth'] = parent_comment.depth + 1
        data['blog_id'] = blog_id
        c = Comment.objects.create(**data)
        c.save()
        c.set_lower_bound()
        if c.path is None:
            c.path = ''
        c.path = ' '.join([c.path, str(-c.lower_bound), str(c.id)])
        c.save()

    @transaction.atomic()
    def update_comment(self, id, data):
        comment = self.get_comment(id)
        for atr in data:
            setattr(comment, atr, data[atr])
        comment.save()
        if 'up_votes' in data or 'down_votes' in data:
            thread = sorted(Comment.objects.filter(path__startswith=comment.path).iterator(),
                            key=lambda c: [float(n) for n in c.path.split()])
            self.update_comment_thread(comment, thread)

    @transaction.atomic()
    def update_comment_thread(self, me, thread):
        lb, depth, my_path_list = me.lower_bound, me.depth, me.path.split()
        for c in thread:
            path_list = c.path.split()
            if path_list[:len(my_path_list)] != my_path_list:
                continue
            c.path = ' '.join(path_list[:depth * 2] + [str(-lb)] + path_list[depth * 2 + 1:])
            c.save()

    def delete_comment(self, id):
        self.get_comment(id).delete()


class Comment(models.Model):
    body = models.TextField()
    _up_votes = models.PositiveIntegerField(default=1)
    _down_votes = models.PositiveIntegerField(default=0)
    _lower_bound = models.FloatField(default=0)
    depth = models.PositiveIntegerField(default=0)
    blog_id = models.PositiveIntegerField(default=0)  # id of Blog Post
    parent = models.PositiveIntegerField(default=None, null=True)
    path = models.TextField(default=None, null=True)
    hidden = models.BooleanField(default=False)

    objects = CommentManager()

    @property
    def up_votes(self):
        return self._up_votes

    @up_votes.setter
    def up_votes(self, value):
        self._up_votes += 1
        self.lower_bound = 1

    @property
    def down_votes(self):
        return self._down_votes

    @down_votes.setter
    def down_votes(self, value):
        self._down_votes += 1
        self.lower_bound = 1

    @property
    def lower_bound(self):
        return self._lower_bound

    @lower_bound.setter
    def lower_bound(self, value):
        # comments = sorted(Comment.objects.filter(path__startswith=self.path).iterator(),
        #                   key=lambda c: [float(n) for n in c.path.split()])
        self.set_lower_bound()

    def set_lower_bound(self):
        n = self.up_votes + self.down_votes
        if n == 0:
            return 0
        pos = self.up_votes
        z = 1.96
        phat = 1.0 * pos / n
        self._lower_bound = (phat + z * z / (2 * n) - z * ((phat * (1 - phat) + z * z / (4 * n)) / n)) / (
                                                                                                             1 + z * z / n) ** 0.5
