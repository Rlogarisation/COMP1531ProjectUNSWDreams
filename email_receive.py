import poplib
import base64
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr


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

    # 关闭与服务器的连接，释放资源
    server.close()

    return msg
if __name__ == "__main__":
    get_email_content()