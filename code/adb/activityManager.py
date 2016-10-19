from adb import ADB


class ActivityManager(object):

    def __init__(self, serial_num):
        self.adb = ADB(serial_num)

    def start_activity(self, pkg, activity):
        return self.adb.exec_shell("am start {0}/.{1}".format(pkg, activity))

    def run_instrument(self, instrument_builder):
        if not instrument_builder:
            raise Exception("Require instrument_builder!")
        # getattr throw exception when "exec_cmd" not found
        if not callable(getattr(instrument_builder, "get_cmd", None)):
            raise Exception("instrument_builder's 'get_cmd' is not callable")
        cmd = instrument_builder.get_cmd()
        return self.adb.exec_shell(cmd, shutup=False)


class InstrumentBuilder(object):
        #   am instrument: start an Instrumentation.  Typically this target <COMPONENT> is the form <TEST_PACKAGE>/<RUNNER_CLASS>.  Options are:
        #   -r: print raw results (otherwise decode REPORT_KEY_STREAMRESULT).  Use with  [-e perf true] to generate raw output for performance measurements.

        #   -p <FILE>: write profiling data to <FILE>
        #   -w: wait for instrumentation to finish before returning.  Required for test runners.
        #   --user <USER_ID> | current: Specify user instrumentation runs in; current user if not specified.
        #   --no-window-animation: turn off window animations while running.
        #   --abi <ABI>: Launch the instrumented process with the selected ABI. This assumes that the process supports the selected ABI.

    def __init__(self):
        self.cmd = "am instrument -w"
        self.test_runner = None

    def get_cmd(self):
        if not self.test_runner:
            raise Exception("test runner not set.")
        return self.cmd + " " + self.test_runner

    def add_test_runner(self, test_runner):
        self.test_runner = test_runner

    #   -e <NAME> <VALUE>: set argument <NAME> to <VALUE>.  For test runners a common form is [-e <testrunner_flag> <value>[,<value>...]].
    def add_report(self, report_name):
        self.cmd += " -e reportFile " + report_name

    def add_scope_package(self, package):
        self.cmd += " -e package " + package

    def add_scope_class(self, package, clazz):
        self.cmd += " -e class {0}.{1}".format(package, clazz)

    def add_scope_method(self, package, clazz, method):
        self.cmd += " -e class {0}.{1}#{2}".format(package, clazz, method)
