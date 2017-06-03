'''
	reference:http://blog.csdn.net/hcf105/article/details/44775977
	set unittest style
'''


import sys
import time
import unittest

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE= -11
STD_ERROR_HANDLE = -12

FOREGROUND_WHITE = 0x0007
FOREGROUND_BLUE = 0x01 # text color contains blue.
FOREGROUND_GREEN= 0x02 # text color contains green.
FOREGROUND_RED  = 0x04 # text color contains red.
FOREGROUND_INTENSITY = 0x08 # text color is intensified.
FOREGROUND_YELLOW = FOREGROUND_RED | FOREGROUND_GREEN

BACKGROUND_BLUE = 0x10 # background color contains blue.
BACKGROUND_GREEN= 0x20 # background color contains green.
BACKGROUND_RED  = 0x40 # background color contains red.
BACKGROUND_INTENSITY = 0x80 # background color is intensified.

import ctypes

std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

def set_color(color, handle=std_out_handle):
    """(color) -> BOOL
    Example: set_color(FOREGROUND_GREEN | FOREGROUND_INTENSITY)
    """
    bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return bool
class _ColorWritelnDecorator:
    """Used to decorate file-like objects with a handy 'writeln' method"""
    def __init__(self, stream):
        self.stream = stream

    def __getattr__(self, name):
        return getattr(self.stream, name)

    def yellow(self, msg):
        set_color(FOREGROUND_YELLOW | FOREGROUND_INTENSITY)
        self.write(msg)
        set_color(FOREGROUND_WHITE)

    def writeln(self, msg=None):
        if msg:
            self.write(msg)
        self.write('\n')

    def red(self, msg):
        set_color(FOREGROUND_RED | FOREGROUND_INTENSITY)
        self.write(msg)
        set_color(FOREGROUND_WHITE)

    def green(self, msg):
        set_color(FOREGROUND_GREEN | FOREGROUND_INTENSITY)
        self.write(msg)
        set_color(FOREGROUND_WHITE)
class MyTestResult(unittest.TestResult):
    separator1 = '[----------] '
    separator2 = '[==========] '
    def __init__(self, stream=sys.stderr, descriptions=1, verbosity=1):
        unittest.TestResult.__init__(self)
        self.stream = stream
        self.showAll = verbosity > 1
        self.dots = verbosity == 1
        self.descriptions = descriptions

    def getDescription(self, test):
        if self.descriptions:
            return test.shortDescription() or str(test)
        else:
            return str(test)

    def startTest(self, test):
        self.stream.green('[ Run      ] ')
        self.stream.writeln(self.getDescription(test))
        unittest.TestResult.startTest(self, test)
        if self.showAll:
            self.stream.write(self.getDescription(test))
            self.stream.write(" ... ")

    def addSuccess(self, test):
        unittest.TestResult.addSuccess(self, test)
        if self.showAll:
            self.stream.writeln("ok")
        elif self.dots:
            self.stream.green('[       OK ] ')
            self.stream.writeln(self.getDescription(test))

    def addError(self, test, err):
        unittest.TestResult.addError(self, test, err)
        if self.showAll:
            self.stream.writeln("ERROR")
        elif self.dots:
            self.stream.write('E')

    def addFailure(self, test, err):
        unittest.TestResult.addFailure(self, test, err)
        if self.showAll:
            self.stream.writeln("FAIL")
        elif self.dots:
            self.stream.red('[  FAILED  ] ')
            self.stream.writeln(self.getDescription(test))
            self.stream.write(self._exc_info_to_string(err, test))


class MyTestRunner:
    def __init__(self, stream=sys.stderr, descriptions=1, verbosity=1):
        self.stream = _ColorWritelnDecorator(stream)
        self.descriptions = descriptions
        self.verbosity = verbosity

    def run(self, test):
        result = MyTestResult(self.stream, self.descriptions, self.verbosity)
        self.stream.yellow('Note: TYMT Unit Tests Starts')
        self.stream.writeln()
        startTime = time.time()
        test(result)
        stopTime = time.time()
        timeTaken = stopTime - startTime
        self.stream.green(result.separator2)
        run = result.testsRun
        self.stream.writeln("Ran %d test%s in %.3fs" %
                            (run, run != 1 and "s" or "", timeTaken))

        failed, errored = map(len, (result.failures, result.errors))

        self.stream.green("[  PASSED  ] %d tests" % (run - failed - errored))
        self.stream.writeln()

        if not result.wasSuccessful():
            errorsummary = ""
            if failed:
                self.stream.red("[  FAILED  ] %d tests, listed below:" % failed)
                self.stream.writeln()
                for failedtest, failederorr in result.failures:
                    self.stream.red("[  FAILED  ] %s" % failedtest)
                    self.stream.writeln()
            if errored:
                self.stream.red("[  ERRORED ] %d tests" % errored)
                for erroredtest, erorrmsg in result.errors:
                    self.stream.red("[  ERRORED ] %s" % erroredtest)
                    self.stream.writeln()

            self.stream.writeln()
            if failed:
                self.stream.write("%d ERRORED TEST" % failed)
            if errored:
                self.stream.write("%d ERRORED TEST" % errored)

        return result