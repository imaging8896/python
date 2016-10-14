class Case(object):

    def test(self):
        raise Exception("Override this method to implement the test.")
        # return True, "message"

    def run(self):
        # DO NOT override this method
        self.setUp()
        isPass, log = self.test()
        self.tearDown()
        return isPass, log
