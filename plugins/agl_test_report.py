import os
import json
from plugins.agl_test_conf import REPORT_LOGS_DIR
from plugins.agl_test_conf import TMP_LOGS_DIR


#Compress the tmp log to .zip, and store the zip file under REPORT_LOGS_DIR/THIS_TEST/
def log_compress(THIS_TEST):
    cmdline = "cd " + TMP_LOGS_DIR + ";" + "zip -q -r " + REPORT_LOGS_DIR + THIS_TEST + "/" + THIS_TEST + ".zip " + "./" +THIS_TEST
    output = os.popen(cmdline)
    output.close()


#Get all test cases status 
#The type of test_cases_values_and_status is list,it's looks like that:
#[['test_id', 'values', 'status'], ['rpm01', 'TEST-PASS', 'passed'],....]
#The type of case_status is directory,it's looks like:
#{'rpm03': 'passed', 'rpm02': 'passed', 'rpm01': 'passed'}
def get_case_status(test_cases_values_and_status):
    num = len(test_cases_values_and_status)
    case_status = {}
    for i in range(num):
        if (i==0):
            continue
        case_status[test_cases_values_and_status[i][0]] = test_cases_values_and_status[i][2]
    return case_status


#Case_status is a dictionary type of data,Record the test name/id and final results of all test cases
#Get the summary of the test case status, the result is like that:
#Summary = [["collected",3],["passed",3],["failed",0],["skipped",0]]
def get_summary(case_status):
    collected_num = passed_num = failed_num = skipped_num = 0
    collected_num = len(case_status)
    for status in case_status.values():
        if (status == "passed"):
            passed_num = passed_num + 1
        elif (status == "failed"):
            failed_num = failed_num + 1
        else:
            skipped_num = skipped_num + 1
    summary = [["collected",collected_num],["passed",passed_num],["failed",failed_num],["skipped",skipped_num]]
    return summary


#Write the test result to a json file under the dir TMP_LOGS_DIR
def write_date_to_json(test_set_status,THIS_TEST,summary,case_status):
    #The data that will be written into the json file
    data =  {
                'test_status': test_set_status,
                'test_name': THIS_TEST,
                'collected': summary[0][1],
                'passed': summary[1][1],
                'failed': summary[2][1],
                'skipped': summary[3][1],
                'case_status': case_status
            }

    #Write the "data" to the json file
    report_json = TMP_LOGS_DIR + THIS_TEST + "/" + "report.json"
    with open(report_json,'w') as f:
        json.dump(data,f,indent=4,sort_keys=False)
    f.close()
