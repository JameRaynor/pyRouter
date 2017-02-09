#coding=utf-8


from dao.DaoFactor import DaoFactor

def queryDB():
    conn = DaoFactor.meepoConn()
    # conn send sql query
    conn.close()
    return