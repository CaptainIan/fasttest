import unittest

class TestLoader(unittest.TestLoader):

    def getTestCaseNames(self, testcase_class)  -> list:
        test_names = super().getTestCaseNames(testcase_class)
        testcase_methods = list(testcase_class.__dict__.keys())
        test_names.sort(key=testcase_methods.index)
        return test_names