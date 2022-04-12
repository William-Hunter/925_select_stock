# -*- coding: UTF-8 -*-
"""
发送邮件的模块
"""

from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
import config


# ssl登录
def login():
    smtp = SMTP_SSL(config.get()['email']['server']['host'])
    # set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
    smtp.set_debuglevel(1)
    smtp.ehlo(config.get()['email']['server']['host'])
    smtp.login(config.get()['email']['server']['username'], config.get()['email']['server']['pwd'])
    return smtp


def sendMail(smtp, receivers, mail_title, mail_content):
    msg = MIMEText(mail_content, "html", 'utf-8')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = config.get()['email']['server']['username']

    words = ','
    receiver_list = words.join(receivers)

    msg["To"] = receiver_list
    smtp.sendmail(config.get()['email']['server']['username'], receivers, msg.as_string())
    smtp.quit()

