# zabbix报警发送数据趋势图片
一般系统已内置python2.7,需安装pip
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python get-pip.py
```
安装依赖
```
sudo pip install requests
```

### 邮件发送脚本
根据实际环境调整`HOST` `user` `password` `period` `smtp_host` `from_email` `passwd`

`sudo cp rtmail.py /usr/lib/zabbix/alertscripts/rtmail.py`
```
设置脚本权限
```
sudo chmod a+x /usr/lib/zabbix/alertscripts/rtmail.py
```
测试脚本执行
```
#ITEM ID需有效
sudo -u zabbix /usr/lib/zabbix/alertscripts/rtmail.py xxx@xxx.com nihao "ITEM ID:23843"
```
### 配置报警媒介
新建报警媒介

- 名称：rtmail
- 类型：脚本
- 脚本名称：rtmail.py
- 脚本参数
    - {ALERT.SENDTO}
    - {ALERT.SUBJECT}
    - {ALERT.MESSAGE}

### 调整报警内容
配置动作，在默认信息中加入ITEMI ID
```
ITEM ID:{ITEM.ID1}
```
### 邮件发送效果
![image](https://note.youdao.com/yws/public/resource/7d986dbc90ebc3b25827a78614c5b782/xmlnote/B518194E8BA748EC9CC22FD5749CA5F2/38789)
