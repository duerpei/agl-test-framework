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
        return 0
    else:
        print("error: {} is not found".format(cmd))
        return 1

#Make dir for THIS_TEST to save the log
def create_dir(THIS_TEST):
    cmdline = "mkdir -p " + TMP_LOGS_DIR + THIS_TEST + "/log/; " + "mkdir -p " + REPORT_LOGS_DIR + ";"
    output = os.popen(cmdline)
    output.close()

# print errors
def printe(msg):
    print("**** ERROR: " + msg)

# print debug info
def printd(msg):
    # TODO
    print("==== DEBUG: " + msg)
