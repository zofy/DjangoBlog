import itertools

from django.db import transaction


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
        elif len(upper) != 0:
            return upper[::-1] + [me], 0
        elif len(lower) != 0:
            return [me] + lower, 1

    @staticmethod
    @transaction.atomic()
    def change_path(path, depth, line):
        for c in line:
            c.path = path + ' ' + ' '.join(c.path.split()[depth + 1:])
            c.save()

    @staticmethod
    def get_line(comments_to_change, comments):
        i, j = 0, 0
        while i < len(comments):
            if j >= len(comments_to_change):
                break
            if comments_to_change[j].id == comments[i].id:
                res = [comment for comment in
                       itertools.takewhile(lambda c: c.path.startswith(comments[i].path), comments[i:])]
                yield res
                j += 1
                i += len(res) - 1
            i += 1

    @classmethod
    def update_sort(cls, me, comments):
        res = cls.to_change(me, cls.check_sorted(comments))
        if res is None:
            return
        comments_to_change = res[0]

        g = cls.get_line(comments_to_change, comments)
        first = g.next()

        p = first[0].path

        for line in g:
            last_path = line[0].path
            if res[1] == 0:
                cls.change_path(last_path, me.depth, first)
                first = line
            elif res[1] == 1:
                line_path = line[0].path
                cls.change_path(p, me.depth, line)
                p = line_path
        if res[1] == 0:
            cls.change_path(p, me.depth, first)
        elif res[1] == 1:
            cls.change_path(p, me.depth, first)
