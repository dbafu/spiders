import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from subprocess import check_output


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

from_addr = 'xdodx@qq.com'
password = 'qftfvkuvoswdbbjf'
to_addr = '2899109958@qq.com'

smtp_server = 'smtp.qq.com'

msg = MIMEText('python爬虫运行异常，异常信息为遇到 HTTP 403', 'plain', 'utf-8')
msg['From'] = _format_addr('一号爬虫 <%s>' % from_addr)
msg['To'] = _format_addr('管理员 <%s>' % to_addr)
msg['Subject'] = Header('一号爬虫运行状态', 'utf-8').encode()
try:
    #qq邮箱要求必须使用 SSL 协议
    server = smtplib.SMTP_SSL(smtp_server, 465) 
    #网易邮箱不强制要求 SSL 协议，可以按如下方式写
    # server = smtplib.SMTP(smtp_server, 25)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
    print('邮件发送成功 ！')
except Exception as e:
    print(e)
