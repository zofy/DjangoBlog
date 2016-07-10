import time
from contextlib import contextmanager


@contextmanager
def time_this(label):
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print('%s: %.10f' % (label, end - start))
