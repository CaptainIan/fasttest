#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import copy
from xffasttest.common import Dict, DictEncoder, gvar
from jinja2 import Environment, FileSystemLoader

RANGES_COLOR = [
    (0, 60, 'color-errors'),
    (61, 80, 'color-failures'),
    (81, 100, 'color-success')
]
class TestReports(object):

    def __init__(self, testresult = None) -> None:

        self.total = len(testresult.result)
        self.errors = len(testresult.errors)
        self.failures = len(testresult.failures)
        self.skipped = len(testresult.skipped)
        self.success = self.total - self.errors - self.failures - self.skipped
        self.duration = testresult.duration
        self.passrate = round((self.success / (self.total - self.skipped)) * 100, 2)
        self.reports = testresult.reports
        self.start_time = int(testresult.start_time) * 1000
        self.end_time = int(testresult.end_time) * 1000
        self.passrate_color = 'color_default'
        for low, high, color in RANGES_COLOR:
            if low <= self.passrate <= high:
                self.passrate_color = color

        self.summary = {
            'total': self.total,
            'errors': self.errors,
            'failures': self.failures,
            'skipped': self.skipped,
            'success': self.success,
            'duration': self.duration,
            'passrate': self.passrate,
            'reports': self.reports,
            'startTime': self.start_time,
            'endTime': self.end_time,
            'passrate_color': self.passrate_color,
            'type': 'UI'
        }
        self.test_cases = []
        self.failure_test_cases = []
        self._parse_report_(testresult.result)
        self.report_data = Dict({
            'summary': self.summary,
            'testCases': self.test_cases,
            'failureTestCases': self.failure_test_cases,
            'users': gvar.config.users
        })
        
    def _parse_report_(self, results: list) -> Dict:
        
        test_cases_data = {}
        failure_test_cases_data = {}
        for result in results:
            file_name = result.file_name.strip('.py')
            key = f'{result.case_module}/{file_name}'
            if key not in test_cases_data:
                test_cases_data[key] = Dict({
                    'path': key,
                    'cases': [],
                    'total': 0,
                    'success': 0,
                    'errors': 0,
                    'failures': 0,
                    'skipped': 0,
                    'duration': 0.0,
                })
            
            if result.status == 1 or result.status == 2:
                status = 'failures' if result.status == 1 else 'errors'
                if key not in failure_test_cases_data: failure_test_cases_data[key] = copy.deepcopy(test_cases_data[key])
                failure_test_cases_data[key].cases.append(result.__dict__)
                failure_test_cases_data[key]['total'] += 1
                failure_test_cases_data[key]['duration'] += result.duration
                failure_test_cases_data[key][status] += 1
                failure_test_cases_data[key]['duration'] = round(failure_test_cases_data[key]['duration'], 2)
            
            test_cases_data[key].cases.append(result.__dict__)
            test_cases_data[key]['total'] += 1
            test_cases_data[key]['duration'] += result.duration

            if result.status == 0: test_cases_data[key]['success'] += 1
            if result.status == 1: test_cases_data[key]['failures'] += 1
            if result.status == 2: test_cases_data[key]['errors'] += 1
            if result.status == 3: test_cases_data[key]['skipped'] += 1
            
            passrate = 0
            success = test_cases_data[key].success
            total = test_cases_data[key].total
            skipped = test_cases_data[key].skipped
            duration = test_cases_data[key].duration
            if total != 0 and (total - skipped) != 0:
                passrate = round((success / (total - skipped)) * 100, 2)
            test_cases_data[key]['passrate'] = passrate
            test_cases_data[key]['duration'] = round(duration, 2)

        self.test_cases = list(test_cases_data.values())
        self.failure_test_cases = list(failure_test_cases_data.values())
    
        
    def generate_reports(self) -> None:
        
        json_data = json.dumps(self.report_data, cls=DictEncoder, indent=4)
        with open(os.path.join(self.reports, 'reports.json'), 'w', encoding='utf-8') as json_file:
            json_file.write(json_data)
        

        resource = os.path.join(os.path.split(os.path.abspath(__file__))[0], "resource")
        env = Environment(loader=FileSystemLoader(resource))

        template = env.get_template('reporter.html')

        rendered_html = template.render(json.loads(json_data))

        with open(os.path.join(self.reports, 'reports.html'), 'w', encoding='utf-8') as html_file:
            html_file.write(rendered_html)