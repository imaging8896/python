import os
from os.path import basename
from os.path import join as pathJoin
from os.path import exists as dirExists
from shutil import move


def move_to(dest):
    def func(src):
        move(src, pathJoin(dest, basename(src)))

    return func


def makedirs_if_not_exist(directory):
    if not dirExists(directory):
        os.makedirs(directory)


def listdir_abs(directory):
    return [pathJoin(directory, x) for x in os.listdir(directory)]


def listdir_abs_filter(directory, filter_func=None):
    """
    >>> this_dir = os.path.abspath(os.path.dirname(__file__))
    >>> test_dir = os.path.abspath(os.path.join(this_dir, "..", "..", "test_data", "test_dir"))
    >>> test_file_1 = os.path.join(test_dir, "1")
    >>> test_file_abc = os.path.join(test_dir, "abc")
    >>> set(listdir_abs_filter(test_dir, None)) == set([test_file_1, test_file_abc])
    True
    >>> set(listdir_abs_filter(test_dir, str.isdigit)) == set([test_file_1])
    True
    >>> set(listdir_abs_filter(test_dir, str.isalpha)) == set([test_file_abc])
    True
    >>> set(listdir_abs_filter(test_dir, not_startswith("a"))) == set([test_file_1])
    True
    >>> set(listdir_abs_filter(test_dir, not_digit())) == set([test_file_abc])
    True
    """
    if filter_func:
        return [x for x in listdir_abs(directory) if filter_func(basename(x))]
    return listdir_abs(directory)


# filter function
def not_startswith(word):
    """
    >>> not_startswith("abc")("abcd")
    False
    >>> not_startswith("abc")("ddabcd")
    True
    >>> not_startswith("abc")("")
    True
    >>> not_startswith("")("")
    False
    >>> not_startswith("")("asd")
    False
    """
    def filter_func(check_one):
        return not check_one.startswith(word)
    return filter_func


# filter function
def startswith(word):
    """
    >>> startswith("abc")("abcd")
    True
    >>> startswith("abc")("ddabcd")
    False
    >>> startswith("abc")("")
    False
    >>> startswith("")("")
    True
    >>> startswith("")("asd")
    True
    """
    def filter_func(check_one):
        return check_one.startswith(word)
    return filter_func


# filter function
def not_digit():
    """
    >>> not_digit()("abcd")
    True
    >>> not_digit()("123")
    False
    >>> not_digit()("123abc")
    True
    """
    def filter_func(check_one):
        return not check_one.isdigit()
    return filter_func
