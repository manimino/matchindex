from hashindex.constants import SIZE_THRESH


def test_collider():
    """
    In CPython, -1 and -2 both hash to -2. A collision we can use for tests!

    This test ensures that is still the case, since other tests rely on that behavior.
    """
    assert hash(-1) == hash(-2) == -2


def test_dict_bucket_collision(index_type):
    """
    Ensure the DictBuckets still work properly under hash collision.
    """
    size_n1 = SIZE_THRESH * 2
    size_n2 = SIZE_THRESH * 3
    items = [{'n': -1} for _ in range(size_n1)] + [{'n': -2} for _ in range(size_n2)]
    hi = index_type(items, ['n'])
    assert len(hi.find({'n': -1})) == size_n1
    assert len(hi.find({'n': -2})) == size_n2
