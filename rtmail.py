#!/usr/bin/env python
# coding=utf-8
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import smtplib
import sys
import os
import time
import re
import logging.handlers
import requests

# 日志输出配置格式
logger = logging.getLogger("root")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("[%(asctime)s %(filename)s:%(lineno)s - %(funcName)15s()] %(message)s")

# 日志输出位置
handler = logging.handlers.RotatingFileHandler("/tmp/altermail_img.log")
handler.setFormatter(formatter)
logger.addHandler(handler)
# zabbix服务器IP
HOST = '127.0.0.1'
# zabbix用户名
user = 'xxx'
# zabbix密码
password = 'xxx'
# 数据间隔时间
period = '3600'
# 图片保存路径
graph_path = '/tmp'
# 邮箱服务器
smtp_host = 'smtp.xxx.com'
# 邮箱账户
from_email = 'xxx@xxx.com'
# 邮箱密码
passwd = 'xxx'


def get_itemid():
    # 获取itemid
    a = re.findall(r"ITEM ID:\d+", sys.argv[3])
    i = str(a)
    itemid = re.findall(r"\d+", i)
    logger.info(itemid)
    return str(itemid).lstrip('[\'').rstrip('\']')


# get grafa#
def get_graph(itemID, pName=None):
    myRequests = requests.Session()
    try:
        """
        获取性能图，首先需要登录
        通过分析，可以直接Post/Get方式登录
        """
        loginUrl = "http://%s/zabbix/index.php" % HOST

        loginHeaders = {
            "Host": HOST,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }

        # 构建登录所需的信息
        playLoad = {
            "name": user,
            "password": password,
            "autologin": "1",
            "enter": "Sign in",
        }

        # 请求登录
        res = myRequests.post(loginUrl, headers=loginHeaders, data=playLoad)
        """
        登入状态后，在POST数据中加入itemid
        """
        testUrl = "http://%s/zabbix/chart.php" % HOST
        testUrlplayLoad = {
            "period": period,
            "itemids[0]": itemID,
            "type": "0",
            "profileIdx": "web.item.graph",
            "width": "700",
        }
        testGraph = myRequests.get(url=testUrl, params=testUrlplayLoad)

        # 返回图片源码，直接保存到本地
        IMAGEPATH = os.path.join(graph_path, pName)
        f = open(IMAGEPATH, 'wb')
        f.write(testGraph.content)
        f.close()
        return IMAGEPATH

    except Exception as e:
        print e
        return False


def text_transfe_html(text):
    # 将message转换为html
    d = text.splitlines()
    html_text = ''
    for i in d:
        i = '' + i + '</br>'
        html_text += i
    return html_text


def send_mail(to_email, subject, picture_name):
    # 发送邮件
    graph_name = get_graph(itemid, picture_name)
    html_text = text_transfe_html(sys.argv[3])
    msg = MIMEMultipart('related')
    fp = open(graph_name, 'rb')
    image = MIMEImage(fp.read())
    fp.close()
    image.add_header('Content-ID', '<image1>')
    msg.attach(image)
    html = """
    <div>
    """
    html += html_text
    html += '<img src="cid:image1"><br/>'
    html += """
    </div>
    """
    html = MIMEText(html, 'html', 'utf8')
    msg.attach(html)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    smtp_server = smtplib.SMTP_SSL()
    smtp_server.connect(smtp_host, '465')
    smtp_server.login(from_email, passwd)
    smtp_server.sendmail(from_email, to_email, msg.as_string())
    smtp_server.quit()


if __name__ == '__main__':
    time_tag = time.strftime("%Y%m%d%H%M%S", time.localtime())
    to = sys.argv[1]
    subject = sys.argv[2]
    subject = subject.decode('utf-8')
    itemid = get_itemid()
    picture_name = time_tag + ".png"
    send_mail(to, subject, picture_name)