#coding=utf-8

import os
import importlib

from tornado.log import access_log as logger


"""
    扫描传入进来的路径下的所有 filter 模块
        filter 函数 存储在 array里, 执行顺序为加载顺序, 即 filter 文件中的位置
        多个 filter 文件, 如何处理加载顺序 ? 因此应该考虑设定 level字段来控制

    扫描传入进来的路径下的所有 controller 模块

"""


__controllerStore={}
__filterStroe=[]

def mapping(uri, open_htqs=False):
    if open_htqs:
        logger.info("Waiting implement...")

    def func_wrapper(func):
        if __controllerStore.get(uri):
            raise Exception("Uri=%s has bean mapped" % uri)

        logger.warn("    |-- mapping: %s --> %s", uri, func.__name__)
        __controllerStore[uri] = func
        return func
    return func_wrapper


def calling(uri):
    return __controllerStore.get(uri, None)



def filtering():
    def func_wrapper(func):
        __filterStroe.append(func)
        logger.warn("    |-- filtering: %s", func.__name__)

        return func
    return func_wrapper


def getFilters():
    return __filterStroe


class Scanner:
    def __init__(self):
        pass


    @staticmethod
    def scaningFilter(filterDir):
        logger.info("Begin Scan all filter...")
        Scanner.scaningMoudel(filterDir)


    @staticmethod
    def scaningCtrller(ctrllerDir):
        logger.info("Begin Scan all controller...")
        Scanner.scaningMoudel(ctrllerDir)


    @staticmethod
    def scaningMoudel(pkgPath):
        if pkgPath.endswith("/"):
            newPath = pkgPath.replace("/", "")
        else:
            newPath = pkgPath.replace("/", ".")

        names=os.listdir(pkgPath)
        for name in names:
            if name.startswith("__init__.py") or not name.endswith(".py"):
                continue

            fileName = name.split(".")[0]
            moduleTmp = "%s.%s" % (newPath, fileName)
            logger.info("  |-- load: %s", moduleTmp)

            importlib.import_module(moduleTmp)
