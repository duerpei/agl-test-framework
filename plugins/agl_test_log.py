import pytest
import os
import re

from agl_test_conf import REPORT_LOGS_DIR
from agl_test_conf import TMP_LOGS_DIR

#WORK_DIR = "/work/duep/agl-test-gitlab/agl-release-tests/"

#process the log like:  -> case_name: TEST-PASS
#                       -> case_name: TEST-FAIL
#                       -> case_name: TEST-SKIP
def log_process_default(log):
    file = open(log)
    count = 0
    test_cases_values_and_status = [["test_id","values","status"]]
    while True:
        txt = file.readline()
        if not txt:
            break
        res = re.search(r'\w+: TEST-\w+',txt)
        if(res != None):
            res = res.group()
            l = ["test_id","values","failed"]
            l[0] = re.search("\w+(?=:)",res).group()
            l[1] = re.search(r'TEST-\w{2,}',res).group()
            test_cases_values_and_status.append(l)

    file.close()
    return test_cases_values_and_status

#Process the log like: TEST-29 FAIL / TEST-30 OK
def log_process_gnome_result(log):
    #
    #  to do process the log of gnome result!!!! 
    #
    file = open(log)
    test_cases_values_and_status = [["test_id","values","status"]]
    while True:
        txt = file.readline()
        if not txt:
            break
        ret = txt.find("TEST-")
    file.close
    test_cases_values_and_status = [["test_id","values","status"],["glib/bookmarkfile.test","PASS",""]]
    return test_cases_values_and_status


