import os


def all_casings(input_string):
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


def list_abspathes_filter_name(directory, filter_func):
    return [os.path.join(directory, x) for x in os.listdir(directory) if filter_func(x)]
    # return [(os.path.join(directory, x), x) for x in os.listdir(directory)]


def file_name(path):
    return path.split("/")[-1]


# filter function
def not_startswith(word):
    def filter_func(check_one):
        return not check_one.startswith(word)
    return filter_func


# filter function
def startswith(word):
    def filter_func(check_one):
        return check_one.startswith(word)
    return filter_func


# filter function
def not_digit():
    def filter_func(check_one):
        return not check_one.isdigit()
    return filter_func

if __name__ == '__main__':
    # path = "/home/test/workspace/python/Utils/Adapter"
    # print list_abspathes_filter_name(path, not_startswith("M"))
    # from functools import partial
    # print list_abspathes_filter_name(path, startswith("M"))
    # print "-" * 40
    # print list_abspathes_filter_name(path, not_digit())
    # print list_abspathes_filter_name(path, str.isdigit)

    # def filter_paths(paths, filter_func, *args):
    #     print args
    #     if len(args) == 1:
    #         return filter(filter_func(args[0]), paths)
    #     elif len(args) == 2:
    #         return filter(filter_func(args[0], args[1]), paths)

    # a = ["asd", "dddd", "aasssssssssss", "as"]
    # print filter(not_startswith("as"), a)
    all_case_list = list(all_casings("asd"))
    print all_case_list
