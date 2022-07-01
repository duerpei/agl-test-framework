import pytest
import os
import re

from plugins.agl_test_conf import REPORT_LOGS_DIR
from plugins.agl_test_conf import TMP_LOGS_DIR

'''
Process the log and init test_cases_values_and_status.

log : the path of default log

default log formate :
    -> case_name: TEST-PASS
    -> case_name: TEST-FAIL
    -> case_name: TEST-SKIP
'''
def log_process_default(log):
    pattern = '^ -> (.+?): (.+?)$'
    parse_result = log_parse(log, pattern)
    test_cases_values_and_status = [["test_id","values","status"]]

    if parse_result:
        for item in parse_result:
            item_result = [item[0], item[1], ""]
            test_cases_values_and_status.append(item_result)

    return test_cases_values_and_status

'''
Process the log create by gnome_desktop_testing
and init test_cases_values_and_status.

log : the path of gnome_desktop_testing log

gnome_desktop_testing log formate:
    PASS: glib/tls-database.test
    FAIL: glib/markup-escape.test
    SKIP: glib/testname.test
'''
def log_process_gnome_desktop_testing(log):
    pattern = '^(PASS|FAIL|SKIP.+?): (.+test?)$'
    parse_result = log_parse(log, pattern)
    test_cases_values_and_status = [["test_id","values","status"]]
    
    if parse_result:
        for item in parse_result:
            item_result = [item[1], item[0], ""]
            test_cases_values_and_status.append(item_result)

    return test_cases_values_and_status

# parse log file with pattern
def log_parse(log, pattern):
    regex = re.compile(pattern, re.MULTILINE)

    test_log = open(log, 'r')
    
    parse_result = []
    line = test_log.readline()
    while line:
        matchs = regex.search(line)
        if matchs:
            groups = matchs.groups()
            parse_result.append(groups)
        line=test_log.readline()
    test_log.close()
    return parse_result

