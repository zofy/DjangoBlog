import itertools


class CommentSorter(object):
    @staticmethod
    def is_sorted(comments):
        for i, c in enumerate(comments[1:]):
            if comments[i].path > c.path: return False
        return True

    @staticmethod
    def to_change(me, comments):
        neighbors = [c for c in comments if c.depth == me.depth and c.path.split()[:-1] == me.path.split()[:-1]]
        # print([c.path for c in neighbors])
        idx = neighbors.index(me)
        # print([c.path for c in neighbors[idx:]])
        upper = [c for c in itertools.takewhile(lambda c: c.lower_bound < me.lower_bound, neighbors[:idx][::-1])]
        lower = [c for c in itertools.takewhile(lambda c: c.lower_bound > me.lower_bound, neighbors[idx + 1:])]

        if len(upper) != 0 and len(lower) != 0:
            raise Exception('Wrongly sorted comments!')

        return max(upper, lower, key=len)

    @staticmethod
    def get_children(id, comments):
        if not CommentSorter.is_sorted(comments):
            comments = sorted(comments, key=lambda c: c.path)
        for i, c in enumerate(comments):
            if c.id == id:
                break
        return [comment for comment in itertools.takewhile(lambda c: c.path.startswith(comments[i].path), comments[i:])]

    @staticmethod
    def change_childrens_path(path, children):
        pass

    @classmethod
    def sort(cls, comments):
        pass

    @classmethod
    def update_sort(cls, me, comments):
        comments_to_change = cls.to_change(me, comments)
        my_children = cls.get_children(me.id, comments)
        for c in comments_to_change:
            cls.change_childrens_path(me.path, cls.get_children(c.id, comments))
            me.path, c.path = c.path, me.path
        cls.change_childrens_path(me.path, my_children)
        # return comments_to_change