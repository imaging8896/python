from os.path import join as pathJoin
from os.path import dirname
from os.path import basename


def all_same(check_list):
    """
    >>> all_same(["abc", "Abc", "aBc"])
    False
    >>> all_same(["abc", "abc", "abC"])
    False
    >>> all_same(["abc", "abc", "abc"])
    True
    >>> all_same([])
    True
    >>> all_same(("abc", "Abc", "aBc"))
    False
    >>> all_same(("abc", "abc", "abC"))
    False
    >>> all_same(("abc", "abc", "abc"))
    True
    >>> all_same(())
    True
    >>> all_same("123")
    False
    >>> all_same("113")
    False
    >>> all_same("111")
    True
    >>> all_same("")
    True
    >>> all_same(None)
    Traceback (most recent call last):
        ...
    TypeError: 'NoneType' object is not iterable
    >>> all_same(123)
    Traceback (most recent call last):
        ...
    TypeError: 'int' object is not iterable
    """
    return all(x == check_list[0] for x in check_list)


def no_duplicate(check_list):
    """
    >>> no_duplicate(["abc", "Abc", "aBc"])
    True
    >>> no_duplicate(["abc", "abc", "abC"])
    False
    >>> no_duplicate([])
    True
    >>> no_duplicate(("abc", "Abc", "aBc"))
    True
    >>> no_duplicate(("abc", "abc", "abC"))
    False
    >>> no_duplicate(())
    True
    >>> no_duplicate("123")
    True
    >>> no_duplicate("113")
    False
    >>> no_duplicate("")
    True
    >>> no_duplicate(None)
    Traceback (most recent call last):
        ...
    TypeError: object of type 'NoneType' has no len()
    >>> no_duplicate(123)
    Traceback (most recent call last):
        ...
    TypeError: object of type 'int' has no len()
    """
    return len(check_list) == len(set(check_list))


def all_casings(input_string):
    """
    >>> set(all_casings("abc")) == set(["abc", "Abc", "aBc", "abC", "ABc", "AbC", "aBC", "ABC"])
    True
    >>> set(all_casings("")) == set([""])
    True
    >>> set(all_casings(None))
    Traceback (most recent call last):
        File "<stdin>", line 1, in ?
    ValueError: Argument should have value.
    """
    if input_string is None:
        raise ValueError("Argument should have value.")
    if not input_string:
        yield ""
    else:
        first = input_string[:1]
        if first.lower() == first.upper():
            for sub_casing in all_casings(input_string[1:]):
                yield first + sub_casing
        else:
            for sub_casing in all_casings(input_string[1:]):
                yield first.lower() + sub_casing
                yield first.upper() + sub_casing


def random_str(length):
    import random
    import string
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(length))


def random_num_str(length):
    import random
    import string
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(length))


def get_all_casings_file(file):
    """
    >>> set(get_all_casings_file("/a/b/c/abc")) == set(["/a/b/c/abc", "/a/b/c/Abc", "/a/b/c/aBc", "/a/b/c/abC", "/a/b/c/ABc", "/a/b/c/AbC", "/a/b/c/aBC", "/a/b/c/ABC"])
    True
    >>> set(get_all_casings_file("abc")) == set(["abc", "Abc", "aBc", "abC", "ABc", "AbC", "aBC", "ABC"])
    True
    >>> set(get_all_casings_file(""))
    Traceback (most recent call last):
        File "<stdin>", line 1, in ?
    ValueError: Argument should have value.
    >>> set(get_all_casings_file(None))
    Traceback (most recent call last):
        File "<stdin>", line 1, in ?
    ValueError: Argument should have value.
    """
    if not file:
        raise ValueError("Argument should have value.")
    for case in all_casings(basename(file)):
        yield pathJoin(dirname(file), case)
