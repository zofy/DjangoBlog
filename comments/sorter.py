class CommentSorter(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CommentSorter, cls).__new__(cls)
        return cls.instance

    def to_change(self, me, comments):
        pass
