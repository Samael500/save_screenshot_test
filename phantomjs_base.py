from memory_profiler import memory_usage
from helpers import test_browser
from settings import USER_AGENT

import subprocess
import os
import time


script_path = 'phantom_screen.js'

def make_param(url, res, save_as):
    script_template = '''
        var page = require('webpage').create();
        page.settings.userAgent = '%s';
        page.viewportSize = { width:%s, height:768 };
        page.open('%s', function (status) {
            page.render('%s');
            phantom.exit();
        });'''
    script = script_template % (USER_AGENT, res, url, save_as)

    with open(script_path, 'w') as phantomjs:
        phantomjs.write(script)

def no_vdisplay_test_browser(path, url, res, save_as, none_2):
    """ create rowser and save img """
    make_param(url, res, save_as)
    res = subprocess.check_call([path, script_path, '--ssl-protocol=any'])

    assert res == 0

def phantomjs_test_browser(name):

    if name == 'phantomjs-no_selenium':
        test_browser('./bin/phantomjs-1.9.8-linux-x86_64/bin/phantomjs', name, None, no_vdisplay_test_browser)

    if name == 'phantomjs2-no_selenium':
        test_browser('./bin/phantomjs-2.0.0/bin/phantomjs', name, None, no_vdisplay_test_browser)
