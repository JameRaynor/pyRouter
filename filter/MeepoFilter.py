#coding=utf-8

import Settings

from core.Scanner import filtering
from core.ServletDispatcher import ServletRequest
from core.ViewMaker import ViewMaker
from core.tools import htqsValidate

"""
增加 htqs 加密拦截
"""



@filtering()
def htqsFilter(httpReq):
    if not isinstance(httpReq, ServletRequest):
        return ViewMaker.httpStatusView(500, "httpReq is not Servlet Request !")

    qsStr = httpReq.get_query_string()
    checkFlag = htqsValidate(Settings.MEEPO_HASH_SALT, Settings.MEEPO_TIME_OUT, qsStr)


    if checkFlag is True :
        return ViewMaker.chainView()
    else:
        return ViewMaker.httpStatusView(500, "Forbidden, HTQS check False ! ")


# @filtering()
# def mkSession(httpReq):
#     if not isinstance(httpReq, ServletRequest):
#         return ViewMaker.httpStatusView(500, "httpReq is not Servlet Request !")
#     return ViewMaker.chainView()
#
#     # dstKey: session_sessionID
#     sessionId = httpReq.get_cookie("TSESSIONID")
#     if sessionId:
#         CacheDao.getCache(sessionId)

