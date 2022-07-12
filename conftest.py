# -*- coding:utf-8 -*-
import pytest
import json
import shutil
import subprocess

from plugins.agl_test_conf import BASE_LOGS_DIR
from plugins.agl_test_conf import TMP_LOGS_DIR
from plugins.agl_test_conf import REPORT_LOGS_DIR


@pytest.fixture(scope='session' ,autouse=True)
def setup_compress_function():
    #Before the test start, clean the env
    args = "ls " + TMP_LOGS_DIR + "report.json"
    output = subprocess.run(args,stdout=subprocess.PIPE,shell=True)
    if(output.returncode == 0):
        args = "rm " + TMP_LOGS_DIR + "report.json"
        subprocess.run(args,shell=True)

    #Makdir of TMP_LOGS_DIR/test-report and REPORT_LOGS_DIR
    args = "mkdir -p " + TMP_LOGS_DIR + "test-report; mkdir -p " + REPORT_LOGS_DIR
    subprocess.run(args,shell=True)

    yield
    #Collect report.json from all test sets to generate a report.json for all the test sets
    args = "find -name report.json>report_files"
    subprocess.run(args,cwd=TMP_LOGS_DIR,shell=True)

    #Get the summary data and write to report.json file
    summary_data = get_summary_data()
    summary_json = TMP_LOGS_DIR + "/report.json"
    with open(summary_json, 'w') as summary_file:
        json.dump(summary_data,summary_file,indent=4,sort_keys=False)
    summary_file.close()

    #Creat summary report in html
    html = get_summary_report_html(summary_data)
    html_path = TMP_LOGS_DIR + "test-report/summary-report.html"
    html_file = open(html_path,"w")
    html_file.write(html)
    html_file.close()

    #Copy summary report file
    source_file = TMP_LOGS_DIR + "test-report/summary-report.html"
    target_file = REPORT_LOGS_DIR + "summary-report.html"
    shutil.copyfile(source_file,target_file)

    #Package the test report
    base_name = REPORT_LOGS_DIR + "agl-test-log-xxx"
    root_dir = TMP_LOGS_DIR + "test-report"
    shutil.make_archive(base_name,"zip",root_dir)

#Summarize all reports.json file
def get_summary_data():
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

            summary_total = summary_total + 1
            if(test_status=="passed"):
                summary_passed = summary_passed + 1
            elif(test_status=="failed"):
                summary_failed = summary_failed + 1
            else:
                summary_skipped = summary_skipped + 1
        f.close()
    summary_data["summary"] = {
        "summary_total": summary_total,
        "summary_passed": summary_passed,
        "summary_failed": summary_failed,
        "summary_skipped": summary_skipped,
    }

    return summary_data

#Generate content for summary report json file
def get_summary_report_html(summary_data):
    status = "fail"
    if(summary_data["summary"]["summary_total"]==summary_data["summary"]["summary_passed"]):
        status = "success"
    html = "<html>"

    #<head> </head>
    html = html + "<head>"
    html = html + "<title>"
    html = html + "Summary Report"
    html = html + "</title>"
    html = html + "</head>"

    #<body> </body>
    html = html + "<body>"
    html = html + "<h1>" + "Summary Report" + "</h1>"
    html = html + "<p>" + "Status :" + status + "</p>"
    html = html + "<p>" + "Total: " + str(summary_data["summary"]["summary_total"])
    html = html + "  Pass: " + str(summary_data["summary"]["summary_passed"])
    html = html + "  Fail: " + str(summary_data["summary"]["summary_failed"])
    html = html + "  Skip: " + str(summary_data["summary"]["summary_skipped"]) + "</p>"
    html = html + "<p>Details : </p>"

    #<table> </table>
    html = html + "<table border=\"1\" cellspacing=\"0\" >"
    html = html + "<tr bgcolor = \"6699ff\">"
    html = html + "<th><font color = \"white\">test suite</font></th>"
    html = html + "<th><font color = \"white\">status</font></th>"
    html = html + "<th><font color = \"white\">pass</font></th>"
    html = html + "<th><font color = \"white\">fail</font></th>"
    html = html + "<th><font color = \"white\">skip</font></th>"
    html = html + "</tr>"

    #Add content to the table
    bgcolor = 0
    for test_suite in summary_data:
        if test_suite == "summary":
            continue
        if bgcolor == 0:
            html = html + "<tr bgcolor = \"66ccff\">"
            bgcolor = 1
        else:
            html = html + "<tr bgcolor = \"66ffff\">"
            bgcolor = 0
        html = html + "<th>" + test_suite + "</th>"
        html = html + "<th>" + summary_data[test_suite]["test_status"] + "</th>"
        html = html + "<th>" + str(summary_data[test_suite]["passed"]) + "</th>"
        html = html + "<th>" + str(summary_data[test_suite]["failed"]) + "</th>"
        html = html + "<th>" + str(summary_data[test_suite]["skipped"]) + "</th>"
        html = html + "</tr>"

    html = html + "</table>"
    html = html + "<p></p>"
    html = html + "<font>Detail log :</font>"
    html = html + "<a href=\"" + "TODO: path to log.zip " + "\">agl-test-log-13.0.1-raspberrypi4-20200808.zip</a>"
    html = html + "</body>"
    html = html + "</html>"

    return html
# TODO:
# Upload the final log to a shared directory or other location
