# -*- coding:utf-8 -*-
import sys
import MySQLdb
import datetime
from op_tools import falcon

project_name_list = ["medweb_online", "op"]
minutes = int(3)
# sentry时间晚了8个小时，每次统计前x分钟的
now = datetime.datetime.now() - datetime.timedelta(hours=8, minutes=minutes)
now_str = now.strftime("%Y-%m-%d %H:%M:%S")

connection = MySQLdb.connect(host="xx.xx.xx.xx", port=13306, user="sentry", passwd="sentryxxx", db="sentry")
cursor = connection.cursor()
metric_list = []
for project_name in project_name_list:
    if project_name == "all":
        sql_format = "select count(1) from sentry_message where datetime > '%s'"
        sql_str = sql_format % now_str
    else:
        sql_format = "select count(1) from sentry_message where datetime > '%s' and project_id in (select id from sentry_project where name = '%s')"
        sql_str = sql_format % (now_str, project_name)

    cursor.execute(sql_str)
    row_result = cursor.fetchone()

    value = row_result[0]
    metric = "sentry_%s" % project_name
    collect_step = 60
    counter_type = "GAUGE"

    info = falcon.build_metric_info(metric, value, collect_step, counter_type,
                                    tags="project=%s,module=sentry" % project_name)
    metric_list.append(info)
falcon.push_metric_info_list_to_falcon(metric_list)
