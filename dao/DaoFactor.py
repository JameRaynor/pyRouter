#coding=utf-8

import MySQLdb
from DBUtils.PooledDB import PooledDB
from tornado.log import access_log as logger

import redis

"""
   Dao 工厂, 统一管理所有数据库联接, 包括redis的联接
"""



class DaoFactor:
    def __init__(self):
        pass

    __connPoolMap={} # 定义私有空间, 存储初始化好的数据库连接池对象: mysql | redis


    @staticmethod
    def initDBPools(dbConfObj):
        if len(DaoFactor.__connPoolMap) > 0:
            logger.info("Pools has been init: ")
            for oneK in DaoFactor.__connPoolMap.keys():
                logger.info("  |-- %s" % oneK)
            return

        if not isinstance(dbConfObj, dict):
            raise Exception("DBPools Init error, dbConfObj is not dict")


        for sourceName in dbConfObj.keys():
            oneCfg = dbConfObj[sourceName]
            if not isinstance(oneCfg, dict):
                raise Exception("Load db cfg, key: %s is not dict, data: %s" % (sourceName, oneCfg))

            cfgData = oneCfg["conf"]
            if not isinstance(cfgData, dict):
                raise Exception("Load db cfg, key: %s conf is not dict, data: %s" % (sourceName, oneCfg))

            if oneCfg["type"] == "mysql":
                poolObj = PooledDB(MySQLdb,
                    mincached=cfgData["min"],
                    maxcached=cfgData["max"],
                    maxconnections=cfgData["max"],
                    host=cfgData["host"],
                    port=cfgData["port"],
                    db=cfgData["db"],
                    user=cfgData["user"],
                    passwd=cfgData["pass"]
                )
            elif oneCfg["type"] == "redis":
                poolObj = redis.ConnectionPool(
                    max_connections=cfgData["max"],
                    host=cfgData["host"],
                    password=cfgData["pass"],
                    port=cfgData["port"],
                    db=cfgData["db"]
                )
            else:
                raise Exception("Load db cfg, key: %s type out of setting, data: %s" % (sourceName, oneCfg))

            # 放入字典, 存储起来这些 pool 对象
            DaoFactor.__connPoolMap[sourceName]=poolObj



    @staticmethod
    def stockConn():
        stockPool = DaoFactor.__connPoolMap["stock"]
        if stockPool:
            return stockPool.connection(shareable=False)
        else:
            return None


    @staticmethod
    def peonConn():
        peonPool = DaoFactor.__connPoolMap["peon"]
        if peonPool:
            return peonPool.connection(shareable=False)
        else:
            return None


    @staticmethod
    def cacheConn():
        pool = DaoFactor.__connPoolMap["redis"]
        if pool:
            return redis.Redis(connection_pool=pool)
        else:
            return None


    @staticmethod
    def meepoConn():
        pass