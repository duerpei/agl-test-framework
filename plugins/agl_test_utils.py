import os

from agl_test_dir_conf import REPORT_LOGS_DIR
from agl_test_dir_conf import TMP_LOGS_DIR


#Check if there is the command that we needed
def find_cmd(cmd):
    cmdline = " which " + cmd
    output = os.popen(cmdline)
    val = output.read()
    output.close()
    ret = val.find(cmd)
    if ret>=0:
        print("{} is found: {}".format(cmd,val))
    else:
        print("error: {} is not found".format(cmd))


#Clean the enviroment, remove the dir of THIS_TEST under TMP_LOGS_DIR and REPORT_LOGS_DIR, and make new dir
def clean_env(THIS_TEST):
    cmdline = "mkdir -p " + TMP_LOGS_DIR + THIS_TEST + "/log/; " + "mkdir -p " + REPORT_LOGS_DIR + ";"
#    cmdline = "cd " + TMP_LOGS_DIR + ";" + "rm -r " + THIS_TEST + ";" + "mkdir -p " + TMP_LOGS_DIR + THIS_TEST + ";" + "cd " + REPORT_LOGS_DIR + ";" + "rm -r " + THIS_TEST + ";" + "mkdir -p " + REPORT_LOGS_DIR + THIS_TEST
    output = os.popen(cmdline)
    output.close()
