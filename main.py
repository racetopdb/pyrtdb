# -*- coding: utf-8 -*-
import unittest
import os
import time
import logging
from Comm.Email import Email
from Comm.Log import log_init
from BeautifulReport import BeautifulReport

# 定义各目录
ProjectHome = os.path.split(os.path.realpath(__file__))[0]
# PageObjectPath = os.path.join(ProjectHome, "Page")
pyrtdbObjectPath = os.path.join(ProjectHome, "pyrtdb")
TestCasePath = os.path.join(ProjectHome, "TestCases")
ReportPath = os.path.join(ProjectHome, "Report")

#对测试结果关键信息进行汇总，做为邮件正文
def summary_format(result):
    summary = "\n" + u"<p>          测试结果汇总信息                </p>" + "\n" + \
                 u"<p> 开始时间: " + result['beginTime'] + u" </p>" + "\n" + \
                 u"<p> 运行时间: " + result['totalTime'] + u" </p>" + "\n" + \
                 u"<p> 执行用例数: " + str(result['testAll']) + u" </p>" + "\n" + \
                 u"<p> 通过用例数: " + str(result['testPass']) + u" </p>" + "\n" + \
                 u"<p> 失败用例数: " + str(result['testFail']) + u" </p>" + "\n" + \
                 u"<p> 忽略用例数: " + str(result['testSkip']) + u" </p>" + "\n"
    return summary

# 发送邮件
'''
def send_email(file, context):
    title = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '自动化测试结果'
    mail = Email(title, context, file)
    send = mail.send_mail()
    if send:
        print('测试报告邮件发送成功')
    else:
        print('测试报告邮件发送失败')
'''


# 加载测试用例
def get_suite(case_path=TestCasePath, rule="test_*.py"):
    """加载所有的测试用例"""
    unittest_suite = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(case_path, pattern=rule, top_level_dir=None)
    for each in discover:
        unittest_suite.addTests(each)
    return unittest_suite

# 执行用例，生成测试报告，并返回报告附件路径、邮件正文内容
def suite_run(unittest_suite):
    """执行所有的用例, 并把结果写入测试报告"""
    run_result = BeautifulReport(unittest_suite)
    now = time.strftime("%Y%m%d%H%M%S", time.localtime())
    filename = now + '_report.html'
    run_result.report(filename=filename, description=now, report_dir=ReportPath)
    rpt_summary = summary_format(run_result.fields)
    return os.path.join(ReportPath, filename), rpt_summary

# 主程序，加载用例，执行用例，发送邮件
if __name__ == "__main__":
    suite = get_suite()
    report_file, report_summary = suite_run(suite)
    print(report_summary)
    # send_email(report_file, report_summary)
