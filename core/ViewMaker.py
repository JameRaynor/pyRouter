#coding=utf-8

import json
import datetime
from tornado.web import RequestHandler


"""
  返回视图对象管理
"""


class DataEncoder( json.JSONEncoder ):
    """ json encoder 处理一些json问题"""
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.__str__()

        return obj.__dict__



class BasicView(object):
    def render(self, reqHandler):
        raise NotImplementedError()



class JsonView(BasicView):
    def __init__(self, dataObj):
        self.dataPkg = dataObj
        pass

    def render(self, reqHandler):
        if not isinstance(reqHandler, RequestHandler):
            raise Exception

        # header set json header
        reqHandler.set_header("Content-Type", "application/json;charset=UTF-8")
        reqHandler.write(json.dumps(self.dataPkg, ensure_ascii=False, cls=DataEncoder))



class StringView(BasicView):
    def __init__(self, stringObj):
        self.dataPkg = stringObj

    def render(self, reqHandler):
        if not isinstance(reqHandler, RequestHandler):
            raise Exception

        reqHandler.set_header("Content-Type", "text/html;charset=UTF-8")
        reqHandler.write(self.dataPkg)



class HtmlView(BasicView):
    def __init__(self, template_name, dataPkg):
        self.templateName=template_name
        self.dataPkg=dataPkg


    def render(self, reqHandler):
        if not isinstance(reqHandler, RequestHandler):
            raise Exception

        reqHandler.render(template_name=self.templateName, dataPkg=self.dataPkg)



class HttpStatusView(BasicView):
    def __init__(self, statusCode, msg):
        self.statusCode=statusCode
        self.msg=msg

    def render(self, reqHandler):
        if not isinstance(reqHandler, RequestHandler):
            raise Exception

        reqHandler.send_error(500, reason=self.msg)


class ChainView(BasicView):
    """该视图, 只是作为 do filter 的类型控制, 并未真正的实现render函数"""
    def __init__(self):
        pass

    def render(self, reqHandler):
        pass



class ViewMaker:
    def __init__(self):
        pass

    @staticmethod
    def jsonView(someObj):
        return JsonView(someObj)


    @staticmethod
    def stringView(stringObj):
        return StringView(stringObj)

    @staticmethod
    def htmlView(template, dataObj):
        pass


    @staticmethod
    def httpStatusView(statusCode, msg):
        return HttpStatusView(statusCode, msg)

    @staticmethod
    def chainView():
        return ChainView()