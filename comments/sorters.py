import itertools


class CommentSorter(object):
    @staticmethod
    def is_sorted(comments):
        for i, c in enumerate(comments[1:]):
            if comments[i].path > c.path: return False
        return True

    @classmethod
    def sort(cls, comments):
        pass

    @classmethod
    def update_sort(cls, id, comments):
        pass

    @staticmethod
    def get_children(id, comments):
        if not CommentSorter.is_sorted(comments):
            comments = sorted(comments, key=lambda c: c.path)
        for i, c in enumerate(comments):
            if c.id == id:
                break
        return [comment for comment in itertools.takewhile(lambda c: c.path.startswith(comments[i].path), comments[i:])]


