#!/usr/bin/python
# -*- coding: utf-8 -*-

# **注意：** python2.6/2.7版本没问题，python3有问题

import smtplib
from email.mime.text import MIMEText
import sys
mail_host = 'smtp.163.com'
mail_user = 'test@163.com'
mail_pass = 'your_mail_password'
mail_postfix = '163.com'


def send_mail(to_list,subject,content):
    me = "zabbix 监控告警平台"+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = me
    msg['to'] = to_list
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me,to_list,msg.as_string())
        s.close()
        return True
    except Exception,e:
        print str(e)
        return False


if __name__ == "__main__":
    send_mail(sys.argv[1], sys.argv[2], sys.argv[3])



