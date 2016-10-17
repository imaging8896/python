import os


def all_casings(input_string):
    """
    >>> set(all_casings("abc")) == set(["abc", "Abc", "aBc", "abC", "ABc", "AbC", "aBC", "ABC"])
    True
    >>> set(all_casings("")) == set([""])
    True
    >>> set(all_casings(None)) == set([""])
    True
    """
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


def list_abspathes_filter_name(directory, filter_func=None):
    """
    >>> this_dir = os.path.abspath(os.path.dirname(__file__))
    >>> test_dir = os.path.abspath(os.path.join(this_dir, "..", "test_data", "test_dir"))
    >>> test_file_1 = os.path.join(test_dir, "1")
    >>> test_file_abc = os.path.join(test_dir, "abc")
    >>> set(list_abspathes_filter_name(test_dir, None)) == set([test_file_1, test_file_abc])
    True
    >>> set(list_abspathes_filter_name(test_dir, str.isdigit)) == set([test_file_1])
    True
    >>> set(list_abspathes_filter_name(test_dir, str.isalpha)) == set([test_file_abc])
    True
    >>> set(list_abspathes_filter_name(test_dir, not_startswith("a"))) == set([test_file_1])
    True
    >>> set(list_abspathes_filter_name(test_dir, not_digit())) == set([test_file_abc])
    True
    """
    if filter_func:
        return [os.path.join(directory, x) for x in os.listdir(directory) if filter_func(x)]
    return [os.path.join(directory, x) for x in os.listdir(directory)]
    # return [(os.path.join(directory, x), x) for x in os.listdir(directory)]


def file_name(path):
    return os.path.basename(path)


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
