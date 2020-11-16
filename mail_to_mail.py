# -*- coding: utf-8 -*-
import smtplib
import string

HOST = 'smtp.163.com'
SUBJECT = 'Test e-mail from Python'
TO = 'yangfang@bbmmgroup.com'
FROM = 'adai_mail@163.com'
text = '人生苦短，我用Python!'
BODY = string.join((
    'From: %s' % FROM,
    'To: %s' % TO,
    'Subject: %s' % SUBJECT,
    '',
    text), '\r\n')
server = smtplib.SMTP()
server.connect(HOST, '25')
server.starttls()
server.login('adai_mail@163.com', 'ZRWXCQXHKPPWJAGB')
server.sendmail(FROM, [TO], BODY)
server.quit()
