# -*- coding:utf-8 -*-
import pytest
import os
import json

from plugins.agl_test_conf import BASE_LOGS_DIR
from plugins.agl_test_conf import TMP_LOGS_DIR
from plugins.agl_test_conf import REPORT_LOGS_DIR

TEST_DIR = "/usr/AGL/agl-test/"

@pytest.fixture(scope='session' ,autouse=True)
def setup_compress_function():
    cmdline = "rm " + REPORT_LOGS_DIR + "/report.json"
    output = os.popen(cmdline)
    output.close()
    yield
    cmdline = "cd " + BASE_LOGS_DIR + "; zip -q -r " + REPORT_LOGS_DIR + "/agl-test-log.zip  ./tmp-log/* ;"
    output = os.popen(cmdline)
    output.close()

    cmd = "cd " + TMP_LOGS_DIR + "; find -name report.json>report_files"
    output = os.popen(cmd)
    output.close()

    summary_data = {}
    summary_total = summary_passed = summary_failed = summary_skipped = 0
    file_path = TMP_LOGS_DIR + "/report_files"
    files = open(file_path)
    while True:
        report = files.readline()
        if not report:
            break
        report = report[1:-1]
        report_json = TMP_LOGS_DIR + report
        with open(report_json,'r') as f:
            data = json.load(f)

            total = passed = failed = skipped = 0
            total = data["collected"]
            passed = data["passed"]
            failed = data["failed"]
            skipped = data["skipped"]
            test_status = data["test_status"]
            test_name = data["test_name"]

            this_summary = {
                'total': total,
                'passed': passed,
                'failed': failed,
                'skipped': skipped,
                'test_status': test_status,
            }
            summary_data[test_name] = this_summary

            summary_total = summary_passed + 1
            if(test_status=="passed"):
                summary_passed = summary_passed + 1
            elif(test_status=="failed"):
                summary_failed = summary_failed + 1
            else:
                summary_skipped = summary_skipped + 1
        f.close()
    print(summary_data)
    summary_data["summary"] = {
        "summary_total": summary_total,
        "summary_passed": summary_passed,
        "summary_failed": summary_failed,
        "summary_skipped": summary_skipped,
    }

    summary_json = REPORT_LOGS_DIR + "/report.json"
    with open(summary_json, 'w') as summary_file:
        json.dump(summary_data,summary_file,indent=4,sort_keys=False)
    summary_file.close()

    # to do:
    # Upload the final log to a shared directory or other location
