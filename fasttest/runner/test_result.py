import os
import sys
import time
import uuid
import unittest
import inspect
from datetime import datetime
from xffasttest.runner import CaseInfo
from xffasttest.common import logger, Fore

STATUS = ['SUCCESS', 'FAILURE', 'ERROR', 'SKIP']
STATUS_COLOR = [Fore.GREEN, Fore.YELLOW, Fore.RED, Fore.WHITE]

class TestResult(unittest.TextTestResult):

    def __init__(self,
                 stream = sys.stderr,
                 descriptions: bool = True,
                 verbosity: int = 1):
        super(TestResult, self).__init__(stream = stream,
                                         descriptions = descriptions,
                                         verbosity = verbosity)
        self.result: list = []

    def startTest(self, test: unittest.TestCase) -> None:
        super(TestResult, self).startTest(test)
        self.start_time = time.time()
        self.result_maessage = None
        self.result_status = None

    def stopTest(self, test: unittest.TestCase) -> None:
        super(TestResult, self).stopTest(test)

        end_time = time.time()
        dt1 = datetime.fromtimestamp( self.start_time)
        dt2 = datetime.fromtimestamp(end_time)
        duration  = round((dt2 - dt1).total_seconds(), 2)
        # test case source code
        test_method = getattr(test.__class__, test._testMethodName)
        case_source = inspect.getsource(test_method)

        case_info = CaseInfo()
        case_desc = test._testMethodDoc.strip() if test._testMethodDoc else test._testMethodDoc
        screenshot_path = os.path.relpath(test.screenshot_path, test.reports) if test.screenshot_path else test.screenshot_path
        video_path = os.path.relpath(test.video_path, test.reports) if test.video_path else test.video_path

        case_info.set_attrs(
            id =  str(uuid.uuid4()),
            reports = test.reports,
            file_name = test.file_name,
            case_module = test.case_module,
            reports_assets = test.reports_assets,
            screenshot_path = screenshot_path,
            video_path = video_path,
            case_name = test._testMethodName,
            case_desc = case_desc,
            case_source = case_source,
            start_time = self.start_time,
            end_time = end_time,
            duration = duration,
            status = self.result_status,
            message = self.result_maessage,
            request = test.request
        )
        self.result.append(case_info)

        # output execution results with messages
        if self.result_maessage and self.result_status:
            logger.log_print(self.separator1, STATUS_COLOR[self.result_status])
            logger.log_print(f'{STATUS[self.result_status]}: {case_info.case_name}', STATUS_COLOR[self.result_status])
            logger.log_print(self.separator2, STATUS_COLOR[self.result_status])
            logger.log_print(self.result_maessage, STATUS_COLOR[self.result_status])

        del self.start_time
        del self.result_maessage
        del self.result_status

    def addSuccess(self, test: unittest.TestCase) -> None:
        super(TestResult, self).addSuccess(test)
        self.result_status = CaseInfo.SUCCESS

    def addError(self, test: unittest.TestCase, err: tuple) -> None:
        super(TestResult, self).addError(test, err)
        self.result_maessage = self._exc_info_to_string(err, test)
        self.result_status = CaseInfo.ERROR

    def addFailure(self, test: unittest.TestCase, err: tuple) -> None:
        super(TestResult, self).addFailure(test, err)
        self.result_maessage = self._exc_info_to_string(err, test)
        self.result_status = CaseInfo.FAILURE

    def addSkip(self, test, reason: str) -> None:
        super(TestResult,self).addSkip(test, reason)
        self.result_maessage = f'{reason} \n'
        self.result_status = CaseInfo.SKIP

    def addExpectedFailure(self, test: unittest.TestCase, err: tuple) -> None:
        super(TestResult, self).addFailure(test, err)
        self.result_maessage = self._exc_info_to_string(err, test)
        self.result_status = CaseInfo.FAILURE
