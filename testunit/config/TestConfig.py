#coding=utf-8

import os, sys
import json

absPath = os.path.abspath(os.path.join(os.path.dirname(__file__))).split(os.path.sep)
appRoot=os.path.sep.join(absPath[:-2]) #项目根目录。-1为上一层, -2 为上二层
print 'appRoot=', appRoot
sys.path.append(appRoot)

"""
 测试 如何 load json格式的配置文件
"""

class ConfBean:
    redissSource = None
    peonSource = None

    def __init__(self):
        self.redisSource = None




def testReadDBConf():
    dbConf = "%s/%s" % (appRoot, "")

    with open(dbConf, 'r') as f:
        obj = json.load(f)

    for key in obj.keys():
        if hasattr(ConfBean(), key):
            print key

        if isinstance(obj[key], dict):
            objSub = obj[key]
            for subKey in objSub.keys():
                print subKey



if __name__ == '__main__':

    testReadDBConf()




