# pyRouter
annotation URL routing for tornado. xliaoong


项目启动[ how to start ]
run: python StartUp.py --port=xxxx
     需要自行指定启动端口, 替换xxxx为想要的端口号即可


依赖环境信息:
    python 2.7
    tornado
    DBUtil
    PooledDB




基于 tornado, 实现自动路由功能

1 关于python修饰器, 有别于java的注解, 两者看似相似实则不同, python的更类似java的AOP模型
     python本身就可以看作一个巨大的IOC模型, 所以python并不用专门支持修饰器的IOC/DI(依赖注入)
     模型, 它自身已经可以动态加载了, 语言特性决定.

2 一些事例:
    @hello
    def foo():
  翻译:
    func = hello(foo)

    @hello1
    @hello2
    def foo():
  翻译:
    func = hello1(hello2(foo))


    @hello(param1, param2)
    def foo():
  翻译:
    func = hello(arg1, arg2)(func)

  因此对于 第二, 第三 两类用法上, 需要修饰器函数hello 的 return 是一个 函数 - funcation