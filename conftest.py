# -*- coding:utf-8 -*-
import pytest
import os

@pytest.fixture(scope='session' ,autouse=True)
def setup_compress_function():
    print("**********test start")
    cmdline = "rm /usr/AGL/agl-test/logs/log-to-report/report.json"
    output = os.popen(cmdline)
    output.close()
    yield
    cmdline = "cd /usr/AGL/agl-test/logs ; zip -q -r /usr/AGL/agl-test/logs/log-to-report/agl-test-log.zip  ./tmp-log/* ;"
    output = os.popen(cmdline)
    output.close()

    print("**********test end")

