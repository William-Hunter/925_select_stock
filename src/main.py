# -*- coding: UTF-8 -*-

import jinrongjie
import time
import config
import mail_work

T1 = time.time()
config._init()


# mail_work.sendMail(mail_work.login(),config.get()['email']['receivers'],"title","concont")


jinrongjie.function()


T2 = time.time()
print('程序运行时间:%s秒' % (round(T2 - T1, 3)))
