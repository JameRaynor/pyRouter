#coding=utf-8

from core.Scanner import mapping
from core.ServletDispatcher import ServletRequest
from core.ViewMaker import ViewMaker
from pojo.json.JsonMsg import MsgMaker

"""
    系统状态查询接口
"""


@mapping("/servlet/status")
def systemStatus(httpReq):
    if not isinstance(httpReq, ServletRequest):
        return ViewMaker.httpStatusView(500, "httpReq is not servlet request !")

    qsStr = httpReq.get_query_string()

    msgObj = MsgMaker.goodMsg()
    msgObj.pushData("QueryString", qsStr)
    return ViewMaker.jsonView(msgObj)


