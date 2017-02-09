#coding=utf-8

import os, sys
absPath = os.path.abspath(os.path.join(os.path.dirname(__file__))).split(os.path.sep)
appRoot=os.path.sep.join(absPath[:-2]) #项目根目录。-1为上一层, -2 为上二层
print 'appRoot=', appRoot
sys.path.append(appRoot)

import Settings
from dao.DaoFactor import DaoFactor
"""
{ key: value, key: value }
"""

def doDaoInitTest():
    DaoFactor.initDBPools(Settings.DB_SETTING_DICT)
    redisClient = DaoFactor.cacheConn()

    print redisClient.keys()


    pass

if __name__ == '__main__':
    doDaoInitTest()