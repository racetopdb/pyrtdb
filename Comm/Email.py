import smtplib
import os
import logging
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.header import Header
from Conf.config import smtp_cfg, email_cfg

_FILESIZE = 20  # 单位M， 单个附件大小
_FILECOUNT = 10  # 附件个数
_smtp_cfg = smtp_cfg
_email_cfg = email_cfg
_logger = logging.getLogger('main.email')


class Email:
    def __init__(self, subject, context=None, attachment=None):
        self.subject = subject
        self.context = context
        self.attachment = attachment
        self.message = MIMEMultipart()
        self._message_init()

    def _message_init(self):
        if self.subject:
            self.message['subject'] = Header(self.subject, 'utf-8')  # 邮件标题
        else:
            raise ValueError("Invalid subject")

        self.message['from'] = _email_cfg['sender']  # from
        self.message['to'] = _email_cfg['receivers']  # to

        if self.context:
            self.message.attach(MIMEText(self.context, 'html', 'utf-8'))  # 邮件正文内容
        # 邮件附件
        if self.attachment:
            if isinstance(self.attachment, str):
                self._attach(self.attachment)
            if isinstance(self.attachment, list):
                count = 0
                for each in self.attachment:
                    if count <= _FILECOUNT:
                        self._attach(each)
                        count += 1
                    else:
                        _logger.warning('Attachments is more than ', _FILECOUNT)
                        break

    def _attach(self, file):
        if os.path.isfile(file) and os.path.getsize(file) <= _FILESIZE * 1024 * 1024:
            attach = MIMEApplication(open(file, 'rb').read())
            attach.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            attach["Content-Type"] = 'application/octet-stream'
            self.message.attach(attach)
        else:
            _logger.error('The attachment is not exist or more than %sM: %s' % (_FILESIZE, file))

    def send_mail(self):
        s = smtplib.SMTP_SSL(_smtp_cfg['host'], int(_smtp_cfg['port']))
        result = True
        try:
            s.login(self._smtp_cfg['user'], self._smtp_cfg['passwd'])
            s.sendmail(self._smtp_cfg['sender'], self._smtp_cfg['receivers'], self.message.as_string())
        except smtplib.SMTPException as e:
            result = False
            _logger.error('Send mail failed', exc_info=True)
        finally:
            s.close()
        return result


'''
调用方法
mail = Email(title, context, file)
send = mail.send_mail()
print(send)

'''