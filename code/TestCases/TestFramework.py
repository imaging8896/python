import traceback
from Utils import config


class Case(object):
    """
        Each test case should inherit this class
    """

    def test(self):
        raise Exception("Override this method to implement the test.")

    def run(self):
        # DO NOT override this method
        try:
            self.setUp()
            self.test()
        except TestAssertionError as tae:
            return False, "In case ({0})\n msg={1}\n stack trace:{2}\n".format(str(self), tae.msg, traceback.format_exc())
        except Exception as e:
            return False, "In class({0}) : {1}\n stack trace : {2}".format(type(self).__name__, e.args, traceback.format_exc())
        finally:
            self.tearDown()
        return True, ""

    def __str__(self):
        return type(self).__name__


class TestSuite(object):
    """
        Each test suite should inherit this class
    """

    def __init__(self):
        self.cases = []
        self.results = []

    def test(self):
        raise Exception("Override this method to implement the test.")

    def add_case(self, case):
        if not isinstance(case, Case):
            raise Exception(
                "'case' argument type is not allowed in test framework, should be TestFramework.Case")
        self.cases += [case]

    def run(self):
        # DO NOT override this method
        # self.setUp() # Currently not need
        self.test()
        for case in self.cases:
            is_pass, msg = case.run()
            if not is_pass:
                self.results += [msg]
        # self.tearDown() # Currently not need
        if self.results:
            return False, "Failed cases number ={0}\n {1}".format(len(self.results), "\n".join(self.results))
        return True, ""


class GlobalSetup(object):

    def __init__(self):
        self.logger = config.get_logger().getChild(
            type(self).__name__ + ".GlobalSetup")

    def run(self):
        pass


class GlobalTeardown(object):

    def __init__(self):
        self.logger = config.get_logger().getChild(
            type(self).__name__ + ".GlobalTeardown")

    def run(self):
        pass


def assert_equal(result, expected, msg=None):
    if not msg:
        msg = "Expected<{0}> but <{1}>".format(expected, result)
    if result != expected:
        raise TestAssertionError(msg)


def assert_not_equal(result, expected, msg=None):
    if not msg:
        msg = "Expected not equal <{0}> but equal".format(expected)
    if result == expected:
        raise TestAssertionError(msg)


def assert_true(result, msg=None):
    if not msg:
        msg = "Expected<True> but <{0}>".format(result)
    if not result:
        raise TestAssertionError(msg)


def assert_false(result, msg=None):
    if not msg:
        msg = "Expected<False> but <{0}>".format(result)
    if result:
        raise TestAssertionError(msg)


def assert_in(result, iterable, msg=None):
    if not msg:
        msg = "Expected in <{0}> but <{1}>".format(iterable, result)
    if result not in iterable:
        raise TestAssertionError(msg)


def assert_not_in(result, iterable, msg=None):
    if not msg:
        msg = "Expected not in <{0}> but <{1}>".format(iterable, result)
    if result in iterable:
        raise TestAssertionError(msg)


class TestAssertionError(Exception):

    def __init__(self, msg):
        self.msg = msg
