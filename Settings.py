#coding=utf-8

"""
  全局配置,
"""


# 系统常量配置
MEEPO_HASH_SALT = "meepo@donar"

MEEPO_TIME_OUT = 1000

MEEPO_CACHE_TIMEOUT = 3600



# 数据库连接池配置
DB_SETTING_DICT={
    "stock" : {
        "type": "mysql",
        "conf": {
            "host": "192.168.1.1",
            "user": "stock",
            "pass": "stock123456",
            "db": "stock",
            "port": 3308,
            "max": 10,
            "min": 2
        }
    },
    "peon" : {
        "type": "mysql",
        "conf": {
            "host": "192.168.1.1",
            "user": "uat",
            "pass": "root123456",
            "db": "peon",
            "port": 3340,
            "max": 10,
            "min": 2
        }
    },
    "redis" : {
        "type": "redis",
        "conf": {
            "host": "192.168.1.1",
            "pass": "redisredis",
            "port": 6403,
            "db": 1,
            "max": 100
        }
    }
}