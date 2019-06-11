#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time

"""
数据迁移:
Tips: 执行脚本前先安装python3，并在目标数据库创建好库
python3 mysql_data_migrate.py
"""

print("*" * 50,"请输入源数据库信息", "*" * 50)
src_db_host = input("Enter source db host:")
src_db_user = input("Enter source db user:")
src_db_pwd = input("Enter source db passwd:")
src_db_name = input("Enter source db name:")

print("*" * 50,"请输入目标数据库信息", "*" * 50)
dest_db_host = input("Enter dest db host:")
dest_db_user = input("Enter dest db user:")
dest_db_pwd = input("Enter dest db passwd:")
dest_db_name = input("Enter dest db name:")

filestamp = time.strftime('%Y-%m-%d-%I:%M')
filename = src_db_name + '-' + filestamp + '.sql'


def export_data():
    """
    数据导出
    :return:
    """
    print("Exporting...")
    os.system("mysqldump --single-transaction -u%s -p%s -h%s %s > %s"% (src_db_user, src_db_pwd, src_db_host, src_db_name, filename))


def import_data():
    """
    数据导入
    :return:
    """
    print("Importing...")
    os.system("mysql -u%s -p%s -h%s %s < %s"% (dest_db_user, dest_db_pwd, dest_db_host, dest_db_name, filename))
    os.remove(filename)


if __name__ == '__main__':
    export_data()
    import_data()




