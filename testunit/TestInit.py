#coding=utf-8
import os, sys

"""
测试用例环境init
"""

absPath = os.path.abspath(os.path.join(os.path.dirname(__file__))).split(os.path.sep)
appRoot=os.path.sep.join(absPath[:-1]) #项目根目录。-1为上一层, -2 为上二层
print 'appRoot=', appRoot
sys.path.append(appRoot)