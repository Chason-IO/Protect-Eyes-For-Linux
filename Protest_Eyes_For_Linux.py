'''
Author: Chason
Date: 2018-05-15 15:53:34
LastEditTime: 2020-08-25 17:47:12
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \GitHub\Blue-Eyes\Protest_Eyes_Linux.py
参考：
http://blog.csdn.net/xuwuhao/article/details/46618913
http://blog.csdn.net/tsing_kou/article/details/53327244
http://blog.sina.com.cn/s/blog_67de9c540102v2np.html
'''

import os
import time
import random
import string
from subprocess import check_output,Popen
import sys

# 当前系统用户名称
Sys_User_Name = "yourcount"
# 当前系统用户密码
Sys_User_Passwd = "yourpasswd"
# 加密原始密码openssl password -1
Original_Passwd = check_output(f"openssl passwd -1 {Sys_User_Passwd}", shell=True).decode('utf-8').strip()

# 休息时间
IntervalTime = 60
Current_Path = os.path.dirname(os.path.abspath(sys.argv[0]))
# 随机密码
Random_Character = ''.join(random.sample(string.ascii_letters + string.digits, 14))
Random_Passwd = check_output(f"openssl passwd -1 {Random_Character}", shell=True).decode('utf-8').strip()
Popen("notify-send -u critical -i battery '温馨提示' '该休息了，注意爱护眼睛～'")
time.sleep(IntervalTime * 1)

# change sys_user passwd with random passwd
os.chdir(Current_Path)
try:
    with open('passwd.txt', 'wb+') as f:
        f.write(Sys_User_Name + ':' + Random_Passwd)
        f.close()
        print('Changing Sys_User Passwd With Random Passwd')
        Popen('/usr/sbin/chpasswd -e < {0}'.format(os.path.join(Current_Path, 'passwd.txt')))
except Exception as e:
    print(e)

# 锁定屏幕
Popen("/usr/bin/xdotool key Ctrl+alt+l")
time.sleep(5)
# 进入屏保状态
Popen("/usr/bin/gnome-screensaver-command -a")
time.sleep(IntervalTime * 3)

os.chdir(Current_Path)
# recover sys_user passwd with original passwd
try:
    with open('passwd.txt', 'wb+') as f:
        f.write(Sys_User + ':' + Original_Passwd)
        f.close()
        print('Recovering Sys_User Passwd With Original Passwd')
        Popen('/usr/sbin/chpasswd -e < {0}'.format(os.path.join(Current_Path, 'passwd.txt')))
except Exception as e:
    print(str(e))

Popen("/usr/bin/gnome-screensaver-command -q")