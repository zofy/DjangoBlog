import itertools
# from comments.models import Comment
import time


class CommentSorter(object):
    @staticmethod
    def check_sorted(comments):
        for i, c in enumerate(comments[1:]):
            if comments[i].path > c.path:
                return sorted(comments, key=lambda c: [int(x) for x in c.path.split()])
        return comments

    @staticmethod
    def to_change(me, comments):
        neighbors = [c for c in comments if c.depth == me.depth and c.path.split()[:-1] == me.path.split()[:-1]]
        idx = neighbors.index(me)
        upper = [c for c in itertools.takewhile(lambda c: c.lower_bound < me.lower_bound, neighbors[:idx][::-1])]
        lower = [c for c in itertools.takewhile(lambda c: c.lower_bound > me.lower_bound, neighbors[idx + 1:])]

        if len(upper) != 0 and len(lower) != 0:
            raise Exception('Wrongly sorted comments!')

        return [me] + max(upper, lower, key=len)

    @staticmethod
    def change_path(path, depth, line):
        for c in line:
            pass
            # c.path = path + ' ' + ' '.join(c.path.split()[depth + 1:])
            # c.save()

    @staticmethod
    def get_line(comments_to_change, comments):
        for i, c in enumerate(comments):
            if c in comments_to_change:
                yield [comment for comment in itertools.takewhile(lambda c: c.path.startswith(comments[i].path), comments[i:])]

    @classmethod
    def update_sort(cls, me, comments):
        comments_to_change = cls.to_change(me, cls.check_sorted(comments))
        # print([c.path for c in comments_to_change])
        g = cls.get_line(comments_to_change, comments)
        first = g.next()
        # print([c.path for c in first])
        p = first[0].path

        start = time.time()
        for line in cls.get_line(comments_to_change, comments):
            last = line[0].path
            cls.change_path(p, me.depth, line)
            p = last

        print(time.time() - start)
        cls.change_path(p, me.depth, first)