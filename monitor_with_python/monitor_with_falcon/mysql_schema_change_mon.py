# -*- coding: utf-8 -*-

import sys
import os
import requests
import time

import pymysql

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, basedir)


class MonMian(object):

    # 初始化参数
    def __init__(self):
        self.t_database = sys.argv[1]
        # tmp_db_con= DataBaseHandle('localhost', 'root', '123456', 'bidata', 3306)
        tmp_db_con = DataBaseHandle('rm-2ze4b4875910y6i98.mysql.rds.aliyuncs.com', 'report', 'fuLBN7jggHr8bRo7',
                                    'bidata', 3306)
        self.db_connect_d = tmp_db_con  # 获取配置表连接

    # 获取基础配置信息
    def getDbDetails(self):
        sql = "select * from mon_mysql_change_details where t_database='{}' ".format(self.t_database)
        db = self.db_connect_d.selectOneDb(sql)
        return db

    # 获取监控表历史字段信息
    def getDbOldSchema(self, t_table):
        sql = "select * from mon_mysql_change_schema where t_database='{}' and t_table='{}' ".format(self.t_database,
                                                                                                     t_table)
        db = self.db_connect_d.selectOneDb(sql)
        return db

    # 获取监控库表字段信息
    def getDbNewSchema(self, t_host, t_password, t_user, t_database):
        db_connect_s = DataBaseHandle(t_host, t_user, t_password, t_database, 3306)
        sql = '''
              select table_name,
                     group_concat(COLUMN_NAME) as column_name 
              from information_schema.columns 
              where table_schema='{}' 
              group by table_schema,table_name
        '''.format(t_database)
        db_schema = db_connect_s.selectDb(sql)
        return db_schema

    # 发消息
    def send_msg(self, msg):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c0f7a0af-272a-4ff1-bc2c-46b5b5eee5a2'
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            'msgtype': 'text',
            'text': {
                "content": msg,
                "mentioned_list": ["@all"],
            },
        }
        r = requests.post(url=url, headers=headers, json=data)
        print r.text

    # 主方法
    def do(self):
        # 获取监控库连接
        db_details = self.getDbDetails()

        # 获取监控库表字段信息
        new_schema = self.getDbNewSchema(db_details.get('t_host'), db_details.get('t_password'),
                                         db_details.get('t_user'), db_details.get('t_database'))
        for items_new in new_schema:
            # 获取监控表历史字段信息
            table_name = items_new.get('table_name')
            old_schema = self.getDbOldSchema(table_name)
            new_column_name = items_new.get('column_name')
            # 配置表未发现此表 ，代表新建表
            if old_schema is None:
                sql = '''
                    insert into mon_mysql_change_schema(t_database,t_table,t_schema) VALUES ('{}','{}','{}')
                '''.format(self.t_database, table_name, new_column_name)

                self.db_connect_d.insertDB(sql)

                msg = "{}库新增{}表".format(self.t_database, table_name)
                self.send_msg(msg)
                time.sleep(3)
                print msg
            else:
                if len(list(set(new_column_name.split(',')) - set(old_schema.get('t_schema').split(',')))) > 0:
                    sql = '''
                        update mon_mysql_change_schema SET t_schema = '{}' WHERE t_database = '{}' and t_table ='{}'
                    '''.format(",".join(new_column_name.split(',')), self.t_database, table_name)

                    self.db_connect_d.updateDb(sql)
                    msg = "{}库{}表新增字段{}".format(self.t_database, table_name, ",".join(
                        list(set(new_column_name.split(',')) - set(old_schema.get('t_schema').split(',')))))

                    self.send_msg(msg)
                    time.sleep(3)
                    print msg

                if len(list(set(old_schema.get('t_schema').split(',')) - set(new_column_name.split(',')))) > 0:
                    sql = '''
                        update mon_mysql_change_schema SET t_schema = '{}' WHERE t_database = '{}' and t_table ='{}'
                    '''.format(",".join(new_column_name.split(',')), self.t_database, table_name)

                    self.db_connect_d.updateDb(sql)

                    msg = "{}库{}表删除字段{}".format(self.t_database, table_name, ",".join(
                        list(set(old_schema.get('t_schema').split(',')) - set(new_column_name.split(',')))))
                    self.send_msg(msg)
                    time.sleep(3)
                    print msg
        self.db_connect_d.closeDb()


class DataBaseHandle(object):
    """定义一个 MySQL 操作类"""

    def __init__(self, host, username, password, database, port):
        '''初始化数据库信息并创建数据库连接'''
        # 下面的赋值其实可以省略，connect 时 直接使用形参即可
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.port = port
        self.db = pymysql.connect(self.host, self.username, self.password, self.database, self.port, charset='utf8',
                                  cursorclass=pymysql.cursors.DictCursor)

    #  这里 注释连接的方法，是为了 实例化对象时，就创建连接。不许要单独处理连接了。
    #
    # def connDataBase(self):
    #     ''' 数据库连接 '''
    #
    #     self.db = pymysql.connect(self.host,self.username,self.password,self.port,self.database)
    #
    #     # self.cursor = self.db.cursor()
    #
    #     return self.db

    def etlLog(self, source_database, source_table_name, exec_flag, msg, script):
        ''' 记录日志 '''
        sql = '''insert into t_pub_etl_log(etl_name,exec_flag,msg,script) values(%s, %s,%s, %s)'''
        args = (source_database + '.' + source_table_name, exec_flag, msg, script)

        self.cursor = self.db.cursor()

        try:
            # 执行sql
            self.cursor.execute(sql, args)
            # tt = self.cursor.execute(sql)  # 返回 插入数据 条数 可以根据 返回值 判定处理结果
            # print(tt)
            self.db.commit()
        except Exception as err:
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()

    def insertDB(self, sql):
        ''' 插入数据库操作 '''

        try:
            # 执行sql
            self.cursor.execute(sql)
            # tt = self.cursor.execute(sql)  # 返回 插入数据 条数 可以根据 返回值 判定处理结果
            # print(tt)
            self.db.commit()
        except Exception as err:
            self.db.rollback()

    def deleteDB(self, sql):
        ''' 操作数据库数据删除 '''
        self.cursor = self.db.cursor()

        try:
            # 执行sql
            self.cursor.execute(sql)
            # tt = self.cursor.execute(sql) # 返回 删除数据 条数 可以根据 返回值 判定处理结果
            # print(tt)
            self.db.commit()
        except Exception as err:
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()

    def updateDb(self, sql):
        ''' 更新数据库操作 '''

        self.cursor = self.db.cursor()

        try:
            # 执行sql
            self.cursor.execute(sql)
            # tt = self.cursor.execute(sql) # 返回 更新数据 条数 可以根据 返回值 判定处理结果
            # print(tt)
            self.db.commit()
        except Exception as err:
            # 发生错误时回滚
            self.db.rollback()

    def selectDb(self, sql):
        ''' 数据库查询 '''

        self.cursor = self.db.cursor()

        try:

            self.cursor.execute(sql)  # 返回 查询数据 条数 可以根据 返回值 判定处理结果
            result = self.cursor.fetchall()  # 返回所有记录列表

            return result
        except Exception as err:
            print('Error: unable to fecth data')

    def selectOneDb(self, sql):
        ''' 数据库查询一条 '''

        self.cursor = self.db.cursor()

        try:
            self.cursor.execute(sql)  # 返回 查询数据 条数 可以根据 返回值 判定处理结果
            result = self.cursor.fetchone()  # 返回所有记录列表
            return result
        except Exception as err:
            print('Error: unable to fecth one data')

    def closeDb(self):
        ''' 数据库连接关闭 '''
        self.db.close()


if __name__ == '__main__':
    db_info = MonMian()
    db_info.do()
