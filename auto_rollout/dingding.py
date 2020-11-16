# -*- coding: utf-8 -*-
import requests
import json
import time
import datetime
from jenkinsapi.jenkins import Jenkins

"""
1. 准备工作
    1.1 创建应用
        1.1.1 AgentId：88****69
        1.1.2 AppKey：ding2***kvqeqsn
        1.1.3 AppSecret：nSaMiTNLQ5E9Yhm0******Xt6JKBRruZHET-
    1.2 应用授权
        1.2.1 通讯录——手机号获取userid权限，测试："userid":"mag***80"
        1.2.2 工作流——审批权限
        1.2.3 待办任务权限
    1.3 应用白名单
    1.3.1 服务器出口ip作为应用ip白名单
    1.4 获取project_id——钉钉工作台某应用id  '/process/get_by_name'
        1.4.1 通用审批: PROC-EC6F39F8-1FBD-4332-B8FB-8CD87EECC1C7
        1.4.2 上线申请: PROC-066DA16E-B68B-424B-8DFA-1B33BABACE59
        1.4.3 紧急上线: PROC-89492106-253F-4EAC-AB55-9D3C2E1C763D
2. 获取工单信息
    2.1 获取token: /gettoken
    2.2 通过token、Appkey、AppSecret、userid获取"上线审批"工单进度: /workrecord/getbyuserid
    2.3 每3分钟执行一次巡检
    2.4 审批通过执行下一步上线操作
3. 进行上线
    3.1 Jenkins创建Webhook：http://jenkins.babamama.cn/jenkins/view/devops/job/nginxtest/buildWithParameters?token=nginxtest&action=deploy
    3.2 提取工单中对应上线项目信息——项目名称
    3.3 拼接 Webhook
    3.4 拼接action 
"""
# 钉钉
Appkey = "dingkv*****kdcpx27t"
Appsecret = "B_H3332GU0sIozvtI*****V4kM1difVpfr_Wb4_hZwulBMZoBR1L7xxSEVu"

process_code = 'PROC-89492106-253F-4EAC-AB55-9D3C2E1C763D'  # 查看 process_code 接口 /process/listbyuserid

# jenkins
username = '***'
password = '***'
jenkins_url = 'http://*****:8080/jenkins/'
server = Jenkins(jenkins_url, username=username, password=password)


def get_timestamp(mins):
    """
    获取n分钟前时间并转换为毫秒级时间戳（钉钉查询必须使用毫秒级时间戳）
    :return: timestamp
    """
    # 获取n分钟前的时间
    mins = int(mins)
    start_time = (datetime.datetime.now() + datetime.timedelta(minutes=-mins)).strftime('%Y-%m-%d %H:%M:%S')
    # 转换为毫秒级时间戳
    start_time_array = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    timestamp = int(round(time.mktime(start_time_array) * 1000))

    return timestamp


def get_token():
    """
    获取Token
    :return: access_token
    """
    url = "https://oapi.dingtalk.com/gettoken?appkey=%s&appsecret=%s" % (Appkey, Appsecret)
    res = requests.get(url)
    access_token = json.loads(res.text)['access_token']

    return access_token


def get_process_id():
    """
    获取待审批任务清单
    :param token:
    :param process_code:
    :param start_time: ts60  每次检查1小时内的审批任务
    :return: task_ids  待审批任务id列表
    """
    url = "https://oapi.dingtalk.com/topapi/processinstance/listids?access_token=%s&process_code=%s&start_time=%s&" \
          "size=%d" % (token, process_code, ts60, 10)
    content = requests.get(url).json()
    task_ids = content['result']['list']

    return task_ids


def start_build_job(task_name):
    """
    创建并发布任务
    :param task_name:
    :return:
    """
    server.build_job(task_name, {'version': 'origin/master'})


def start_deploy():
    """
    执行上线
    :param token:
    :param id:
    :return:
    """
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if len(id_list) == 0:
        print(current_time + ' ' + 'No tasks to deploy!!!')
    else:
        for task_id in id_list:
            url = 'https://oapi.dingtalk.com/topapi/processinstance/get?access_token=%s&process_instance_id=%s' % (
                token, task_id)
            content = requests.get(url).json()

            if len(content) > 0:
                task_name = content['process_instance']['form_component_values'][0]['value'].strip('[|]').strip('\"')
                task_info = content['process_instance']['tasks']
                # print(task_info)
                task_status = task_info[0]['task_status']
                task_result = task_info[0]['task_result']
                task_finish_time = task_info[0]['finish_time']  # 任务审批完成时间 "2020-11-16 13:31:55"

                finish_time_array = time.strptime(task_finish_time, "%Y-%m-%d %H:%M:%S")
                finish_timestamp = int(round(time.mktime(finish_time_array) * 1000))

                # 创建一个3分钟前的时间戳
                ts3 = int(get_timestamp(3))

                if task_status == 'COMPLETED' and task_result == 'AGREE' and finish_timestamp >= ts3:
                    start_build_job(task_name)
                    print(current_time + ' ' + task_name + ' ' + 'Updated!!!')
                else:
                    print(current_time + ' ' + 'No tasks to deploy!!!')


if __name__ == '__main__':
    ts60 = get_timestamp(60)
    token = get_token()
    id_list = get_process_id()
    start_deploy()
