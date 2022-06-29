import os

from plugins.agl_test_conf import REPORT_LOGS_DIR
from plugins.agl_test_conf import TMP_LOGS_DIR


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


#Make dir for THIS_TEST to save the log
def create_dir(THIS_TEST):
    cmdline = "mkdir -p " + TMP_LOGS_DIR + THIS_TEST + "/log/; " + "mkdir -p " + REPORT_LOGS_DIR + ";"
    output = os.popen(cmdline)
    output.close()
