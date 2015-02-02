#coding=utf-8
__author__ = 'junyu'
import MySQLdb

class DaoBaseService:
    host_ip = "42.96.201.101"
    #host_ip = 'localhost'
    usr_name = "www"
    #usr_name = "root"
    password = "52logsucc"
    #password = 'a13870093884'
    db = "www"
    #db = 'test'
    def insert(self, sql, parms):
        try:
             conn=MySQLdb.connect(host=self.host_ip,user=self.usr_name,passwd=self.password,db=self.db,charset="utf8")
             cursor = conn.cursor()
             for parm in parms:
                n = cursor.execute(sql, parm)
             conn.commit()
        except Exception, msg:
             print(msg)
             return
        finally:
            cursor.close()
            conn.close()

    #返回插入主键
    def insert_id(self, sql, parm):
        try:
             conn=MySQLdb.connect(host=self.host_ip,user=self.usr_name,passwd=self.password,db=self.db,charset="utf8")
             cursor = conn.cursor()
             n = cursor.execute(sql, parm)
             id = int(cursor.lastrowid)
             conn.commit()
        except Exception, msg:
             print(msg)
             return
        finally:
            cursor.close()
            conn.close()
        return id


    def query(self,sql):
        try:
            conn=MySQLdb.connect(host=self.host_ip,user=self.usr_name,passwd=self.password,db=self.db,charset="utf8")
            cursor = conn.cursor()
            cursor.execute(sql)
            obj = cursor.fetchall()
        except Exception, msg:
            print msg
            return None
        finally:
            cursor.close()
            conn.close()
        return obj


    def update(self, sql):
        try:
             conn=MySQLdb.connect(host=self.host_ip,user=self.usr_name,passwd=self.password,db=self.db,charset="utf8")
             cursor = conn.cursor()
             cursor.execute(sql)
             conn.commit()
        except Exception, msg:
             print(msg)
             return
        finally:
            cursor.close()
            conn.close()

    def delete(self, sql):
        self.update(sql)