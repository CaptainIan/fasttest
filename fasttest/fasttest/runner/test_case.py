import os
import sys
import unittest
from xffasttest.common import logger, Fore

class TestCase(unittest.TestCase):
    case_info = {}
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.hook_set_up = self.case_info.set_up
        self.hook_tear_down = self.case_info.tear_down
        self.reports = self.case_info.reports
        self.file_name = self.case_info.file_name
        self.case_module = self.case_info.case_module
        self.reports_assets = self.case_info.reports_assets
        self.screenshot_path = self.case_info.screenshot_path
        self.video_path = self.case_info.video_path
        self.request = self.case_info.request

    def run(self, result: unittest.TestResult) -> None:
        logger.log_info(f"******************* TestCase {self._testMethodName} Start *******************", Fore.GREEN)
        unittest.TestCase.run(self, result)
        total = result.testsRun
        errors = len(result.errors)
        failures = len(result.failures)
        skipped = len(result.skipped)
        success: int = total - errors - failures - skipped
        logger.log_info(f"******************* Total: {total} Success: {success} Failed: {failures} "
                        f"Error: {errors} Skipped: {skipped} ********************", Fore.GREEN)

    def setUp(self) -> None:
        try:
            self.hook_set_up(self)
        except Exception as e:
            raise e

    def tearDown(self) -> None:
        try:
            self.hook_tear_down(self)
        except Exception as e:
            raise e

