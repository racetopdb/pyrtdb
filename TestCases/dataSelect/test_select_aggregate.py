#coding=utf-8
import subprocess
import time

#
# filepath="E:/rtdbPython/plugin/python/TestData/test_write_script_win.bat"
#
# # p = subprocess.Popen(filepath, shell=True,stderr=subprocess.STDOUT, stdout = subprocess.PIPE)
# p = subprocess.Popen(r"E:\rtdbPython\plugin\python\TestData\test_write_script_win.bat", creationflags=subprocess.CREATE_NEW_CONSOLE )
# time.sleep(30)
#
# print(p)
#
# stdout, stderr = p.communicate()
#
# print(p.returncode) # is 0 if success




# def cmd_test():
#     # cmd = 'cmd.exe d:/start.bat'
#     p = subprocess.Popen("cmd.exe /c" + "E:\\rtdbPython\\plugin\\python\\TestData\\test_write_script_win.bat", stdout=subprocess.PIPE,
#                          stderr=subprocess.STDOUT)
#     curline = p.stdout.readline()
#
#     while (curline != b''):
#         print(curline)
#         curline = p.stdout.readline()
#     p.wait()
#     print(p.returncode)
#
# if __name__ == '__main__':
#     cmd_test()