from django.db import transaction


class CommentUpdater(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CommentUpdater, cls).__new__(cls)
        return cls.instance

    def get_line(self, me, comments):
        for i, c in enumerate(comments):
            if c.id == me.id:
                break
        while i < len(comments) and comments[i].path.startswith(me.path):
            yield comments[i]
            i += 1

    @transaction.atomic()
    def update_line(self, me, comments):
        lb, depth = me.lower_bound, me.depth
        for c in self.get_line(me, comments):
            path_list = c.path.split()
            c.path = ' '.join(path_list[:depth * 2] + [str(-lb)] + path_list[depth * 2 + 1:])
            c.save()
