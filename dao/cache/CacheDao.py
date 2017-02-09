#coding=utf-8

from dao.DaoFactor import DaoFactor

"""
对接redis, 读取数据, 清理数据
"""


def getDataAsDict(dstKey):
    """ Return a Python dict of the hash's name/value pairs"
    :param dstKey:
    :return:
    """
    redisCli = DaoFactor.cacheConn()
    return redisCli.hgetall(dstKey)


def cachData(dstKey, dstValue, expireTime):
    """ expireTime 过期时间, 单位为 s
    :param dstKey:
    :param dstValue:
    :param expireTime:
    :return:

    """
    if isinstance(expireTime, (int, long)):
        redisCli = DaoFactor.cacheConn()
        return redisCli.setex(dstKey, dstValue, expireTime)

    return False

def getCache(dstKey):
    redisCli = DaoFactor.cacheConn()
    return redisCli.get(dstKey)

