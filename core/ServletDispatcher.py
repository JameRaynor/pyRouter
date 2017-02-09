# coding=utf-8
from tornado.web import RequestHandler
from tornado.log import access_log as logger

from core.Scanner import calling, getFilters
from core.ViewMaker import BasicView, ChainView

"""
when url is:
    full_url: http://127.0.0.1:8000/servlet/test?abc

so request has:
    uri: /servlet/test?abc
    path: /servlet/test
    query: abc

"""


class ServletDispatcher( RequestHandler ):

    def get(self, *args, **kwargs):
        try:
            # 自动路由匹配, 选取预设的对应function
            reqPath = self.request.path
            calledFunc = calling( reqPath )
            if calledFunc is None:
                self.send_error( status_code=404 )
                return

            #执行filter函数, 并获取处理结果
            for usFilter in getFilters():
                viewObj = usFilter( ServletRequest( self ) )
                if not isinstance( viewObj, BasicView ):
                    self.send_error( status_code=500, reason="ViewObj is not BasicView: %s" % reqPath )
                    return

                # 如果是 chainView, 执行下一个filter
                if isinstance(viewObj, ChainView):
                    continue

                # 遇到其它视图, 直接中断处理, 返回该视图
                viewObj.render( reqHandler=self )
                return

            # 执行实例函数, 获取视图结果
            viewObj = calledFunc( ServletRequest( self ) )
            if not isinstance( viewObj, BasicView ):
                self.send_error( status_code=500, reason="viewObj is Not BasicView: %s" % reqPath )
                return

            viewObj.render( reqHandler=self )

        except Exception as e:
            logger.exception(e)
            self.send_error( status_code=500, reason=e.message )

    def post(self, *args, **kwargs):
        self.get( self, args, kwargs )
        pass

    def data_received(self, chunk):
        pass


class ServletRequest:
    """ 对 RequestHandler 的再封装
        来控制 request 只能提取 request 信息, 不能做response动作
        response 动作只能交给封装好的 view 对象来统一处理

        标准化 接口开发流程, 降低接口开发繁复度
    """

    def __init__(self, httpReq):
        if not isinstance( httpReq, RequestHandler ):
            raise Exception

        self.__httpReq = httpReq
        self.session = None


    def get_argument(self, name):
        return self.__httpReq.get_argument( name=name, default=None )

    def get_query_string(self):
        return self.__httpReq.request.query

    def get_uri(self):
        return self.__httpReq.request.path

    def get_header(self):
        return self.__httpReq.request.headers

    def get_body(self):
        return self.__httpReq.request.body

    def get_remote_ip(self):
        return self.__httpReq.request.remote_ip

    def get_host(self):
        return self.__httpReq.request.host

    def get_full_url(self):
        return self.__httpReq.request.full_url

    def get_cookie(self, name):
        return self.__httpReq.get_cookie(name)

    def set_cookie(self, name, value, exprie):
        return self.__httpReq.set_cookie(name=name, value=value, expires=exprie)

    def set_session(self, session):
        self.session = session

    def get_session(self):
        return self.session


class SessionData:
    """
        https://github.com/zs1621/tornado-redis-session
        https://github.com/XxxUNIXxxX/TornadoSessions
    """
    def __init__(self, sessionId, salt):
        self.sessionId = sessionId
        self.salt = salt
        pass

