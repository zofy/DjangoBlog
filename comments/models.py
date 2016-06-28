from django.db import models


class Comment(models.Model):
    body = models.TextField()
    up_votes = models.PositiveIntegerField(default=0)
    down_votes = models.PositiveIntegerField(default=0)
    _lower_bound = models.FloatField(default=0)
    depth = models.PositiveIntegerField(default=0)
    parent = models.PositiveIntegerField(null=True)  # id of Blog Post
    path = models.TextField(null=True)
    hidden = models.BooleanField(default=False)

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
