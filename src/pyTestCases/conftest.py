import pytest
# pytest print out config
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    out = yield
    report = out.get_result()
    if(report.when == "call"):
        print("\n====================================================")
        print('Test Result:\t%s' % out)    
        print('Test Report:\t%s' % report)
        print('Process:\t%s' % report.when)
        print('id:\t%s' % report.nodeid)
        print('description:\t%s' % str(item.function.__doc__))
        print('result:\t%s' % report.outcome)
    
    