import subprocess

from plugins.agl_test_conf import REPORT_LOGS_DIR
from plugins.agl_test_conf import TMP_LOGS_DIR


#Check if there is the command that we needed
def find_cmd(cmd):
    args = " which " + cmd
    output = subprocess.run(args,stdout=subprocess.PIPE,shell=True)
    output.returncode
    if output.returncode==0:
        return 0
    else:
        print("error: {} is not found".format(cmd))
        return 1

#Make dir for THIS_TEST to save the log
def create_dir(THIS_TEST):
    args = "mkdir -p " + TMP_LOGS_DIR + THIS_TEST + "/log/; mkdir -p " + TMP_LOGS_DIR + "test-report/" + THIS_TEST
    output = subprocess.run(args,shell=True)

# print errors
def printe(msg):
    print("**** ERROR: " + msg)

# print debug info
def printd(msg):
    # TODO
    print("==== DEBUG: " + msg)
