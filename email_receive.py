import poplib
import base64
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import time
from datetime import date, datetime, timezone, tzinfo, timedelta


def parser_subject(msg):
    subject = msg['Subject']
    value, charset = decode_header(subject)[0]
    if charset:
        value = value.decode(charset)
    print('邮件主题： {0}'.format(value))
    return value


def parser_address(msg):
    hdr, addr = parseaddr(msg['From'])
    # name 发送人邮箱名称， addr 发送人邮箱地址
    name, charset = decode_header(hdr)[0]
    if charset:
        name = name.decode(charset)
    print('发送人邮箱名称: {0}，发送人邮箱地址: {1}'.format(name, addr))


def parser_content(msg):
    content = msg.get_payload()

    # 文本信息
    print("内容 :", content)
    print("获得的reset code :", list(content.split())[-1:][0])


def get_email_content():
    useraccount = 'styuannj@163.com'
    password = 'UXRVCTIAEQZVVGAG'

    # 邮件服务器地址,以下为网易邮箱
    pop3_server = 'pop.163.com'

    # 开始连接到服务器
    server = poplib.POP3(pop3_server)

    # 打开或者关闭调试信息，为打开，会在控制台打印客户端与服务器的交互信息
    server.set_debuglevel(1)

    # 打印POP3服务器的欢迎文字，验证是否正确连接到了邮件服务器
    print(server.getwelcome().decode('utf8'))

    # 开始进行身份验证
    server.user(useraccount)
    server.pass_(password)

    # 返回邮件总数目和占用服务器的空间大小（字节数）， 通过stat()方法即可
    email_num, email_size = server.stat()
    print("消息的数量: {0}, 消息的总大小: {1}".format(email_num, email_size))

    # 使用list()返回所有邮件的编号，默认为字节类型的串
    rsp, msg_list, rsp_siz = server.list()
    print("服务器的响应: {0},\n消息列表： {1},\n返回消息的大小： {2}".format(rsp, msg_list, rsp_siz))

    print('邮件总数： {}'.format(len(msg_list)))

    # 下面单纯获取最新的一封邮件
    total_mail_numbers = len(msg_list)
    rsp, msglines, msgsiz = server.retr(total_mail_numbers)
    #print("服务器的响应: {0},\n原始邮件内容： {1},\n该封邮件所占字节大小： {2}".format(rsp, msglines, msgsiz))

    msg_content = b'\r\n'.join(msglines).decode('gbk')

    msg = Parser().parsestr(text=msg_content)
    print('解码后的邮件信息:\n{}'.format(msg))

    date_time = msg["Date"].split()
    print("发送时间 == ", msg['Date'])
    print("发送时间 == ", date_time[3], datetime.strptime(date_time[2], '%b').tm_mon, date_time[1], date_time[4])

    # 关闭与服务器的连接，释放资源
    server.close()

    return msg


if __name__ == '__main__':
    # # 返回解码的邮件详情
    # msg = get_email_content()
    # # 解析邮件主题
    # parser_subject(msg)
    # # 解析发件人详情
    # parser_address(msg)
    # # 解析内容
    # parser_content(msg)
    print(datetime.now())
    print(datetime.utcnow())
    print(datetime.utcnow().replace(tzinfo=timezone.utc))
    print(datetime.now() + timedelta(seconds=time.timezone))

    print(datetime.now().timestamp())
    print(datetime.utcnow().timestamp())
    print(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())
    print((datetime.now() + timedelta(seconds=time.timezone)).replace(tzinfo=timezone.utc).timestamp())

    datetime.strptime(datetime.now(), '%a, %d %b %Y %H:%M:%S %Z')
