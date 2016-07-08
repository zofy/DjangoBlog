import itertools

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
        upper = [c for c in itertools.takewhile(lambda c: c.lower_bound < me.lower_bound, neighbors[:idx][::-1])][::-1]
        lower = [c for c in itertools.takewhile(lambda c: c.lower_bound > me.lower_bound, neighbors[idx + 1:])]

        if len(upper) != 0 and len(lower) != 0:
            raise Exception('Wrongly sorted comments!')
        elif len(upper) != 0:
            return upper + [me]
        elif len(lower) != 0:
            return [me] + lower

    @staticmethod
    def change_path(path, depth, line):
        for c in line:
            c.path = path + ' ' + ' '.join(c.path.split()[depth + 1:])
            c.save()

    @staticmethod
    def get_children2(comments_to_change, comments):
        output, i, j = [], 0, 0
        while i < len(comments):
            if comments_to_change[j] == comments[i]:
                output.append([comment for comment in
                               itertools.takewhile(lambda c: c.path.startswith(comments[i].path), comments[i:])])
                j += 1
                i += len(output[-1]) - 1
            i += 1
        return output

    @classmethod
    def update_sort(cls, me, comments):
        comments_to_change = cls.to_change(me, cls.check_sorted(comments))
        depth = me.depth
        print([c.path for c in comments_to_change])

        for i, line in enumerate(comments[1:]):
            path = line[0].path
            cls.change_path(path, depth, comments[i])
