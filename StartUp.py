#coding=utf-8


import tornado.httpserver
import tornado.ioloop
import tornado.web
import Settings

from tornado.log import access_log as logger
from tornado.options import options, define
from core.ServletDispatcher import ServletDispatcher
from core.Scanner import Scanner
from dao.DaoFactor import DaoFactor




"""
start command:
    python -u StartUp.py --port=6001


TODO:
  1 重构启动函数, 更优雅的调用方式来启动
  2 启动顺序, 启动内容, 参考java 工程化
  3 优雅的关闭, 优雅的处理最后的资源回收

  4 是否可以关闭 日志: [I 161220 19:25:30 web:1946] 200 GET /servlet/loaduser?uname=Ffg (127.0.0.1) 37.46ms
  5 确保日志是输入到我指定文件内, 目前看来不是

TODO:
  1 增加 htqs 加密拦截, 可以采用参数判断
  2 mapping 解密函数, 动态装配接口安全的加解密内容

TODO:
  1 DaoFactor 进一步封装硬编码的 key 信息, 封装cfg对象, 封装整个 json格式 配置文件的读取
  2 scaningMoudel 拼写错误

"""

define('port')

def startAll():
    # 验证端口是否配置
    options.parse_command_line()
    if options.port is None:
        logger.info("Start server fail, port is null")
        return

    # init db connection
    DaoFactor.initDBPools(Settings.DB_SETTING_DICT)

    # 加载所有的 filter method
    Scanner.scaningFilter("filter/")

    # 加载所有的 controller method
    Scanner.scaningCtrller("controller/")


    # 启动 web Server
    logger.info("Start sever, take port is: %s", options.port)
    http_server = tornado.httpserver.HTTPServer(tornado.web.Application([
        (r"/servlet/(.*)", ServletDispatcher),
    ]))
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    startAll()
