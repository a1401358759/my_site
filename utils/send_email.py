# -*- coding: utf-8 -*-

import smtplib
from email.MIMEText import MIMEText


class MailTemplate(object):
    notify_blogger = u'''
        <h4>您的博客上有新的评论啦~</h4>
        <p>“{nickname}”在您的博客上发表了评论:</p>
        <p>“{comment}”</p>
        <p>点击<a href="{target_url}{anchor}">评论内容</a>查看</p>
    '''
    notify_parent_user = u'''
        <p>致：{parent_user}</p>
        <p>您在杨学峰博客上的评论“{parent_comment}”已经获得答复。</p>
        <p>点击<a href="{target_url}{anchor}">评论内容</a>查看</p>
        <p>本邮件为自动发送，请勿直接回复</p>
    '''


class SendEmailClient(object):

    def __init__(self):
        self.mail_host = 'smtp.qq.com'  # 邮件服务器
        self.send_user = u'杨学峰博客'  # 发送方信息
        self.sender = 'yxfblog@qq.com'  # 发送方邮箱
        self.mail_pass = 'nzdptqtwssfibadj'  # 邮箱密码或授权码

    def send_email(self, subject, receivers, mail_body):
        """
        subject: str 邮件主题，
        receivers: list 邮件接收人，
        mail_body: html 邮件内容
        """
        # 邮件内容设置
        message = MIMEText(mail_body, _subtype='html', _charset='utf-8')
        message['Subject'] = subject  # 邮件主题
        message['From'] = self.send_user  # 发送方信息
        message['To'] = ','.join(receivers)  # 接受方信息
        # 登录并发送邮件
        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, 465, timeout=10)
            smtpObj.login(self.sender, self.mail_pass)
            smtpObj.sendmail(self.sender, receivers, message.as_string())
            smtpObj.quit()
            return True, ''
        except smtplib.SMTPException as e:
            return False, e
