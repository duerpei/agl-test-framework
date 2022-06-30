import pytest
import os
import re

from plugins.agl_test_conf import REPORT_LOGS_DIR
from plugins.agl_test_conf import TMP_LOGS_DIR

#Process the log like and get test_cases_values_and_status
#log : the path of source log
#mode : the type of log to process
def log_process_default(log,mode):
    #default log looks like :
    #   -> case_name: TEST-PASS
    #   -> case_name: TEST-FAIL
    #   -> case_name: TEST-SKIP
    pattern_default_line = re.compile('\w+: TEST-\w+')
    pattern_default_id = re.compile("\w+(?=:)")
    pattern_default_value = re.compile('TEST-\w{2,}')

    #gnome_desktop_testing result log, looks like:
    #   PASS: glib/tls-database.test
    #   FAIL: glib/markup-escape.test
    #   SKIP: glib/testname.test
    pattern_gnome_line = re.compile('[PFS][AK][SI][SLP]\w*:\B.+test')
    pattern_gnome_id = re.compile('(?<=/).+')
    pattern_gnome_value = re.compile('\w+(?=:)')

    pattern_list = [[pattern_default_line,pattern_default_id,pattern_default_value],[pattern_gnome_line,pattern_gnome_id,pattern_gnome_value]]
    pattern_num = 0
    if(mode == "gnome"):
        pattern_num = 1

    file = open(log)
    count = 0
    test_cases_values_and_status = [["test_id","values","status"]]
    while True:
        txt = file.readline()
        if not txt:
            break
        res = re.search(pattern_list[pattern_num][0],txt)
        if(res != None):
            res = res.group()
            test_id = re.search(pattern_list[pattern_num][1],res)
            value = re.search(pattern_list[pattern_num][2],res)
            if(value != None and test_id !=None):
                l = [" "," "," "]
                l[0] = test_id.group()
                l[1] = value.group()
                test_cases_values_and_status.append(l)

    file.close()
    return test_cases_values_and_status

