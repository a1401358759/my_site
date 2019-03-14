# -*- coding: utf-8 -*-

'''发送邮件工具'''

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from utils.libs.config import settings


def send_mail(subject, from_addr, to_addrs, content, text_type='plain', accept_language='zh-CN', accept_charset='ISO-8859-1,utf-8'):
    '''向指定联系人发送html邮件

    subject -- 主题
    from_addr -- 发送人，注意：发送人不是可以随便指定的，有的邮件服务商拒绝发送发件人和实际账号不匹配的邮件
    to_addrs -- 收件人。如果为list，则发给一批人，如果为string，则发送给一人
    content -- 邮件内容字符串
    text_type -- subtype of text/* MIME documents. 纯文本邮件为plain, html邮件为html
    '''
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = ', '.join(to_addrs) if isinstance(to_addrs, list) else to_addrs
    msg["Accept-Language"] = accept_language
    msg["Accept-Charset"] = accept_charset
    msg.attach(MIMEText(content, text_type, "utf-8"))

    mail_conf = settings.MAIL_CONFIG
    smtp = smtplib.SMTP_SSL(mail_conf['host'], mail_conf['port'], timeout=5)
    smtp.login(mail_conf['user'], mail_conf['password'])
    smtp.sendmail(from_addr, to_addrs, msg.as_string())
    smtp.quit()
