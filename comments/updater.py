from django.db import transaction


class CommentUpdater(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CommentUpdater, cls).__new__(cls)
        return cls.instance

    @transaction.atomic()
    def update_comment_thread(self, me, comments):
        lb, depth, my_path_list = me.lower_bound, me.depth, me.path.split()
        for c in comments:
            path_list = c.path.split()
            if path_list[:len(my_path_list)] != my_path_list:
                continue
            c.path = ' '.join(path_list[:depth * 2] + [str(-lb)] + path_list[depth * 2 + 1:])
            c.save()
