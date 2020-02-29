# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText


class MailTemplate(object):
    notify_blogger = '''
        <table style="width: 99.8%;height:99.8% ">
           <tbody>
            <tr>
             <td>
              <div style="border-radius: 10px 10px 10px 10px;font-size:13px;color: #555555;width: 666px;font-family:'Century Gothic','Trebuchet MS','Hiragino Sans GB',微软雅黑,'Microsoft Yahei',Tahoma,Helvetica,Arial,'SimSun',sans-serif;margin:50px auto;border:1px solid #eee;max-width:100%;background: #ffffff repeating-linear-gradient(-45deg,#fff,#fff 1.125rem,transparent 1.125rem,transparent 2.25rem);box-shadow: 0 1px 5px rgba(0, 0, 0, 0.15);">
               <div style="width:100%;background:#49BDAD;color:#ffffff;border-radius: 10px 10px 0 0;background-image: -moz-linear-gradient(0deg, rgb(67, 198, 184), rgb(255, 209, 244));background-image: -webkit-linear-gradient(0deg, rgb(67, 198, 184), rgb(255, 209, 244));height: 66px;">
                <p style="font-size:15px;word-break:break-all;padding: 23px 32px;margin:0;background-color: hsla(0,0%,100%,.4);border-radius: 10px 10px 0 0;">您的<a style="text-decoration:none;color: #ffffff;" href="https://yangsihan.com"> 杨学峰博客 </a>上有新的评论啦！ </p>
               </div>
               <div style="margin:40px auto;width:90%">
                <p>{nickname} 发表评论：</p>
                <div style="background: #fafafa repeating-linear-gradient(-45deg,#fff,#fff 1.125rem,transparent 1.125rem,transparent 2.25rem);box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);margin:20px 0px;padding:15px;border-radius:5px;font-size:14px;color:#555555;">{comment}</div>
                <p><a style="text-decoration:none; color:#12addb" href="{target_url}{anchor}" target="_blank">[查看评论]</a></p>
               </div>
              </div> </td>
            </tr>
           </tbody>
          </table>
        </body>
    '''

    notify_parent_user = '''
        <table style="width: 99.8%;height:99.8% ">
           <tbody>
            <tr>
             <td>
              <div style="border-radius: 10px 10px 10px 10px;font-size:13px;color: #555555;width: 666px;font-family:'Century Gothic','Trebuchet MS','Hiragino Sans GB',微软雅黑,'Microsoft Yahei',Tahoma,Helvetica,Arial,'SimSun',sans-serif;margin:50px auto;border:1px solid #eee;max-width:100%;background: #ffffff repeating-linear-gradient(-45deg,#fff,#fff 1.125rem,transparent 1.125rem,transparent 2.25rem);box-shadow: 0 1px 5px rgba(0, 0, 0, 0.15);">
               <div style="width:100%;background:#49BDAD;color:#ffffff;border-radius: 10px 10px 0 0;background-image: -moz-linear-gradient(0deg, rgb(67, 198, 184), rgb(255, 209, 244));background-image: -webkit-linear-gradient(0deg, rgb(67, 198, 184), rgb(255, 209, 244));height: 66px;">
                <p style="font-size:15px;word-break:break-all;padding: 23px 32px;margin:0;background-color: hsla(0,0%,100%,.4);border-radius: 10px 10px 0 0;">您在<a style="text-decoration:none;color: #ffffff;" href="https://yangsihan.com"> 杨学峰博客 </a>上的留言有新回复啦！ </p>
               </div>
               <div style="margin:40px auto;width:90%">
                <p>{parent_user} 同学，您曾在文章上发表评论：</p>
                <div style="background: #fafafa repeating-linear-gradient(-45deg,#fff,#fff 1.125rem,transparent 1.125rem,transparent 2.25rem);box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);margin:20px 0px;padding:15px;border-radius:5px;font-size:14px;color:#555555;">{parent_comment}</div>
                <p>{comment_user} 给您的回复如下：</p>
                <div style="background: #fafafa repeating-linear-gradient(-45deg,#fff,#fff 1.125rem,transparent 1.125rem,transparent 2.25rem);box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);margin:20px 0px;padding:15px;border-radius:5px;font-size:14px;color:#555555;">{comment}</div>
                <p>您可以点击 <a style="text-decoration:none; color:#12addb" href="{target_url}{anchor}">查看回复的完整內容 </a>，欢迎再次光临 <a style="text-decoration:none; color:#12addb" href="https://yangsihan.com"> 杨学峰博客 </a>。</p>
               </div>
              </div> </td>
            </tr>
           </tbody>
        </table>
    '''


class SendEmailClient(object):

    def __init__(self):
        self.mail_host = 'smtp.qq.com'  # 邮件服务器
        self.send_user = 'yxfblog@qq.com'  # 发送方信息
        self.sender = 'yxfblog@qq.com'  # 发送方邮箱
        self.mail_pass = 'xeaxnhwlgdchiaee'  # 邮箱密码或授权码

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
