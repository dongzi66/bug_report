# -*- coding: utf-8 -*-
#!/usr/bin/env python

# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QString', 2)

try:
    import diagramscene_rc3
except ImportError:
    import diagramscene_rc2

from PyQt4 import QtGui
from jimLib.ui.App import MainWindow
from jimLib.ui.Login import login
from jimLib.lib.business import business
import paho.mqtt.client as mqtt

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def on_connect(client, userdata, rc):
    #print("Connected with result code "+str(rc))
    topic = "bug/%s"%user_name
    client.subscribe(topic)

def on_message(client, userdata, msg):
	#print(msg.topic+" "+str(msg.payload))
    #调用消息提示
    mainWindow.touch_sig(str(msg.payload))

    # pass

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)

    mainWindow = MainWindow()
    #登录界面
    loginWindow = login()
    loginWindow.setupUi(loginWindow)
    is_login_ok = False
    my_business = business()
    global user_name
    while not is_login_ok:
        if loginWindow.exec_():
            #print "user_name:%s\n"%loginWindow.user_name
            #print "passwd:%s\n"%loginWindow.passwd
            #检查用户名和密码是否正确
            (message,status,admin_id) = my_business.login(loginWindow.user_name, loginWindow.passwd)
            user_name = loginWindow.user_name
            if status:
                #发送成功消息
                mainWindow.set_message(u'提示',message)
                mainWindow.set_tray(1)
                is_login_ok = True
                #查询我的bug
                (status,is_success,message) = my_business.get_my_bug(admin_id)
                #500,,参数错误 | 200,0,严重错误 | 200,1,一般错误 | 200,-1,没有错误 | 其他查询失败
                if 500 == status:

                    pass
            else:
                #发送错误消息
                mainWindow.set_message(u'错误',message)
                pass


    #开启mqtt推送
    my_client = mqtt.Client()
    my_client.on_connect = on_connect
    my_client.on_message = on_message
    my_client.connect("192.168.1.131", 1883, 60)
    my_client.loop_start()
    mainWindow.my_time()
    #主界面
    mainWindow.setGeometry(100, 100, 800, 500)
    mainWindow.showMaximized()

    sys.exit(app.exec_())
