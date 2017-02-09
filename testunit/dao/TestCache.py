#coding=utf-8
"""
测试 redis 的有关使用
"""

import os, sys
absPath = os.path.abspath(os.path.join(os.path.dirname(__file__))).split(os.path.sep)
appRoot=os.path.sep.join(absPath[:-2]) #项目根目录。-1为上一层, -2 为上二层
print 'appRoot=', appRoot
sys.path.append(appRoot)

import Settings
from dao.DaoFactor import DaoFactor
from dao.cache import CacheDao


def testCacheDao():
    DaoFactor.initDBPools(Settings.DB_SETTING_DICT)

    print CacheDao.getCache("Banlist")
    print CacheDao.cachData("Banlist", "this.is.testt", "12a")


if __name__ == '__main__':
    testCacheDao()




