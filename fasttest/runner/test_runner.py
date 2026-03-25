#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import time
import unittest
from datetime import datetime
from xffasttest.runner.test_result import TestResult
from xffasttest.runner.test_reports import TestReports


class TestRunner(unittest.TextTestRunner):

    def __init__(self, 
                 stream = sys.stderr,
                 descriptions: bool = True,
                 verbosity: int = 1,
                 testresult = None,
                 hook: dict = {},
                 reports: str = None) -> None:
        unittest.TextTestRunner.__init__(self)

        if testresult is None:
            self.testresult = TestResult
        else:
            self.testresult = testresult
        
        self.result = self.testresult(stream=stream,
                                      descriptions=descriptions,
                                      verbosity=verbosity)
        self.result.reports = reports
        self.hook = hook

    def _setUpModule(self) -> None:
        try:
            self.hook.set_up_global()
        except Exception as e:
            raise e

    def _tearDownModule(self) -> None:
        try:
            self.hook.tear_down_global()
        except Exception as e:
            raise e

    def run(self, test) -> object:
        start_time = time.time()
        self._setUpModule()
        test(self.result)
        self._tearDownModule()
        end_time = time.time()
        dt1 = datetime.fromtimestamp(start_time)
        dt2 = datetime.fromtimestamp(end_time)
        self.result.duration = round((dt2 - dt1).total_seconds(), 2)
        self.result.start_time = start_time
        self.result.end_time = end_time

        test_reports = TestReports(self.result)
        test_reports.generate_reports()
        
        return self.result




