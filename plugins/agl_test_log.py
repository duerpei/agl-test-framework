import pytest
import os

from agl_test_dir_conf import REPORT_LOGS_DIR
from agl_test_dir_conf import TMP_LOGS_DIR

#WORK_DIR = "/work/duep/agl-test-gitlab/agl-release-tests/"

#process the log like:  -> rpm02: TEST-PASS
def log_process_default(log):
    file = open(log)
    count = 0
    test_cases_values_and_status = [["test_id","values","status"]]
    while True:
        txt = file.readline()
        if not txt:
            break
        ret = txt.find("TEST-PASS")
        if ret > 0:
            key_end = ret - 2
            key_start = txt.rfind("->",0,key_end) + 3
            l = ["test_id","values","failed"]
            l[0] = txt[key_start:key_end]
            l[1] = "TEST-PASS"
            test_cases_values_and_status.append(l)
            count = count + 1

        ret = txt.find("TEST-FAIL")
        if ret > 0:
            key_end = ret - 2
            key_start = txt.rfind("->",0,key_end) + 3
            l = ["test_id","values","failed"]
            l[0] = txt[key_start:key_end]
            l[1] = "TEST-FAIL"
            test_cases_values_and_status.append(l)
            count = count + 1

    file.close

    return test_cases_values_and_status

#Process the log likeL: TEST-29 FAIL / TEST-30 OK
def log_process_001(log):
    file = open(log)
    test_cases_values_and_status = [["test_id","values","status"]]
    while True:
        txt = file.readline()
        if not txt:
            break
        ret = txt.find("TEST-")
        if ret >= 0:
            l = ["test_id","values","failed"]
            test_id_end = txt.find(" ")
            l[0] = txt[ret:test_id_end]
            if (txt[test_id_end+1]=="O"):
                l[1] = "OK"
            if (txt[test_id_end+1]=="F"):
                l[1] = "FAIL"
            test_cases_values_and_status.append(l)
    file.close
    return test_cases_values_and_status


