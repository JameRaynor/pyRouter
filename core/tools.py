#coding=utf-8

import urllib
import hashlib
import time

"""
 工具类, 以及适量的静态常量

"""

def htqsValidate(salt, timeout, queryStr):
    queryMap = queryStrToMap(queryStr)
    if not queryMap:
        return False

    reqHash = queryMap.pop("hash")
    reqTime = long(queryMap.pop("time"))

    # 验证请求过期
    curTime = long(time.time())
    if (curTime - reqTime/1000) > long(timeout):
        return False

    # 验证Hash
    dstHash = queryStrToMap(htqsEncode(salt, reqTime, queryMap)).pop("hash")
    return dstHash.lower().__eq__(reqHash.lower())


def htqsEncode(salt, timestamp, paramMap):
    if not isinstance(paramMap, dict):
        raise Exception("paramMap is not dict object")

    if not paramMap:
        return None

    queryString = ""
    for key in sorted(paramMap):
        key = str(key).strip()
        dstValue = urllib.quote_plus(str(paramMap[key]).strip())

        temp = "%s=%s" % (key, dstValue)
        queryString = "%s&%s" % (queryString, temp)

    if queryString == "":
        hashStr = hashlib.md5("time=%s&salt=%s" % (timestamp, salt))

        return "time=%s&hash=%s" % (timestamp, hashStr.hexdigest())
    else:
        queryString = queryString.strip("&")
        hashStr = hashlib.md5("%s&time=%s&salt=%s" % (queryString, timestamp, salt))
        return "%s&time=%s&hash=%s" % (queryString, timestamp, hashStr.hexdigest())


def queryStrToMap(queryStr):
    if not isinstance(queryStr, str):
        raise Exception("queryStr is not String object")

    if not queryStr:
        return None

    queryArray = queryStr.split("&")
    if not queryArray:
        return None

    queryMap={}
    for queryKV in queryArray:
        kvArray = queryKV.split("=")
        if not kvArray:
            continue

        queryKey = kvArray[0]
        if len(kvArray) == 2:
            queryValue = kvArray[1]
        else:
            pos = queryKV.find("=")
            queryValue = queryKV[pos+1: len(queryKV)]
        queryMap.__setitem__(queryKey, urllib.unquote_plus(queryValue))

    return queryMap


def mapToQueryStr(queryMap):
    if not isinstance(queryMap, dict):
        raise Exception("paramMap is not dict object")

    if not queryMap:
        return None

    queryString = ""
    for key in queryMap.keys():
        key = str(key).strip()
        dstValue = urllib.quote_plus(str(queryMap[key]).strip())

        temp = "%s=%s" % (key, dstValue)
        queryString = "%s&%s" % (queryString, temp)

    return queryString