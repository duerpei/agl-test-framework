import json
import shutil

from plugins.agl_test_conf import REPORT_LOGS_DIR
from plugins.agl_test_conf import TMP_LOGS_DIR


#Compress the tmp log to .zip, and store the zip file under TMP_LOGS_DIR/test-report
def log_compress(THIS_TEST):
    base_name = TMP_LOGS_DIR + "test-report/" + THIS_TEST + "/log"
    root_dir = TMP_LOGS_DIR + THIS_TEST + "/log"
    shutil.make_archive(base_name,'zip',root_dir)


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

def get_report_html(THIS_TEST,test_set_status,summary,case_status):
    html = "<html>"

    #<head> </head>
    html = html + "<head>"
    html = html + "<title>"
    html = html + THIS_TEST + "test report"
    html = html + "</title>"
    html = html + "</head>"

    #<body> </body>
    html = html + "<body>"
    html = html + "<h1>" + THIS_TEST + " test report" + "</h1>"
    html = html + "<p>" + "Status :" + test_set_status + "</p>"
    html = html + "<p>" + "Total: " + str(summary[0][1])
    html = html + "  Pass: " + str(summary[1][1])
    html = html + "  Fail: " + str(summary[2][1])
    html = html + "  Skip: " + str(summary[3][1]) + "</p>"
    html = html + "<p>Details : </p>"

    #<table> </table>
    html = html + "<table border=\"1\" cellspacing=\"0\" >"
    html = html + "<tr bgcolor = \"6699ff\">"
    html = html + "<th><font color = \"white\">test case</font></th>"
    html = html + "<th><font color = \"white\">status</font></th>"
    html = html + "</tr>"

    #Add content to the table
    bgcolor = 0
    for test_case in case_status:
        if bgcolor == 0:
            html = html + "<tr bgcolor = \"66ccff\">"
            bgcolor = 1
        else:
            html = html + "<tr bgcolor = \"66ffff\">"
            bgcolor = 0
        html = html + "<th>" + test_case + "</th>"
        html = html + "<th>" + case_status[test_case] + "</th>"
        html = html + "</tr>"

    html = html + "</table>"
    html = html + "<p></p>"
    html = html + "<font>Detail log :</font>"
    html = html + "<a href=\"" + THIS_TEST + "/log.zip" + "\">log.zip</a>"
    html = html + "</body>"
    html = html + "</html>"

    return html

def write_to_html_file(THIS_TEST,html):
    html_path = TMP_LOGS_DIR + "test-report/" + THIS_TEST + "/report.html"
    html_file = open(html_path,"w")
    html_file.write(html)
    html_file.close()
