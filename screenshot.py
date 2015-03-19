from selenium import webdriver
from memory_profiler import memory_usage
import os
import time


URL_LIST = ('http://google.com/', 'https://www.facebook.com/', 'http://habrahabr.ru/', 'http://wbtech.pro/', )
RES_LIST = (240, 780, 1320, 1920)
ATTEMPTS = 10

get_img_name = lambda base_path, url, res: '{base_path}/{url}-{res}px.png'.format(
    base_path=base_path, url=url.replace('http:', '').replace('https:', '').replace('/', ''), res=res)

avg = lambda arr: sum(arr) / len(arr)


def save_shot(url, width, browser, save_as):
    """ Open page and save screenshot """
    browser.set_window_size(width, 768)
    browser.get(url)
    browser.save_screenshot(save_as)


def _test_browser(Browser, binary, path, url, res, save_as):
    """ create rowser and save img """
    browser = Browser(**binary) if binary else Browser(path)
    save_shot(url, res, browser, save_as)
    browser.quit()

def _report(log_path, save_as, mins, maxs, avgs, times):
    # make report
    with open(log_path + '.log', 'a') as report:
        report.write(save_as + '\n')
        report.write('min: {value}\n'.format(value=min(mins)))
        report.write('max: {value}\n'.format(value=max(maxs)))
        report.write('avg: {value}\n'.format(value=avg(avgs)))
        report.write('time: {value}\n'.format(value=avg(times)))
        report.write('\n')
    with open(log_path + '-min.log', 'a') as report:
        report.write('{0};{1};{2};{3}\n'.format(min(mins), max(maxs), avg(avgs), avg(times)))

def _report_path(browser_name):
    # base path
    base_path = os.path.join('img', browser_name)
    log_path = os.path.join('report_log')
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    log_path = os.path.join('log', browser_name)
    # clear report
    with open(log_path + '.log', 'w') as report:
        report.write('')
    with open(log_path + '-min.log', 'w') as report:
        report.write('')
    return base_path, log_path


def test_browser(Browser, binary, path, browser_name):
    """ for each site, for each screen """
    base_path, log_path = _report_path(browser_name)
    for url in URL_LIST:
        for res in RES_LIST:
            save_as = get_img_name(base_path, url, res)
            mins = []
            maxs = []
            avgs = []
            times = []
            for i in xrange(ATTEMPTS):
                start = time.time()
                memory = memory_usage((_test_browser, (Browser, binary, path, url, res, save_as)))
                end = time.time()
                mins.append(min(memory))
                maxs.append(max(memory))
                avgs.append(avg(memory))
                times.append(end - start)
            _report(log_path, save_as, mins, maxs, avgs, times)

def get_browser(name):
    """ Get browser webdriver """
    path = bin = None
    if name is 'firefox':
        from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
        binary = FirefoxBinary('bin/firefox/firefox-bin')
        driver = webdriver.Firefox
        bin = dict(firefox_binary=binary)
    elif name is 'chrome':
        assert False
    elif name is 'chromium':
        assert False
    elif name is 'splash':
        assert False
    elif name is 'phantomjs':
        driver = webdriver.PhantomJS
        path = 'bin/phantomjs-1.9.8-linux-x86_64/bin/phantomjs'

    return driver, bin, path, name

if __name__ == '__main__':
    test_browser(*get_browser('phantomjs'))
    time.sleep(30)
    test_browser(*get_browser('firefox'))
