import smtplib, imaplib, poplib, ssl, socket
from libs.path.config_loader import env

def smtp(
        host:str=env("SMTP_HOST"), 
        port:int=env("SMTP_PORT"), 
        user:str= env("MAIL_USER"),
        pwd:str= env("MAIL_PWD"),
        ssl_context=ssl.create_default_context(),
        timeout:float=20
):
    try:
        mail = smtplib.SMTP(host=host, port=port, timeout=timeout)
        mail.ehlo()
        mail.starttls(context=ssl_context)
        mail.ehlo()
        mail.login(user=user, password=pwd)
        return mail
    except(smtplib.SMTPException, TimeoutError, ConnectionRefusedError, Exception) as e:
        raise Exception("Error al conectarse al servidor SMTP: %s" % e)
    except:
        raise Exception("Error al conectarse al servidor SMTP.")
    
def imap(
        host:str=env("IMAP_HOST"), 
        port:int=env("IMAP_PORT"), 
        user:str= env("MAIL_USER"),
        pwd:str= env("MAIL_PWD"),
        timeout:float=20,
        ssl_context=ssl.create_default_context()
):
    try:
        socket.setdefaulttimeout(timeout)
        m = imaplib.IMAP4_SSL(host=host, port=port, timeout=20, ssl_context=ssl_context)
        m.login(user=user, password=pwd)
        return m
    except (imaplib.IMAP4_SSL.error, TimeoutError, ConnectionRefusedError, Exception) as e:
        raise Exception("Error al conectarse al servidor IMAP: %s" % e)
    except:
        raise Exception("Error desconocido al conectarse al servidor IMAP.")
    
def pop(host:str=env("POP_HOST"), 
                port:int=env("POP_PORT"), 
                user:str= env("MAIL_USER"),
                pwd:str= env("MAIL_PWD"),
                timeout:float=20
):
    try:
        socket.setdefaulttimeout(timeout)
        pop = poplib.POP3_SSL(host=host, port=port)
        pop.user(user)
        pop.pass_(pwd)
        return pop
    except (TimeoutError, ConnectionRefusedError, Exception) as e:
        raise Exception("Error al conectarse al servidor POP: %s" % e)
    except:
        raise Exception("Error desconocido al conectarse al servidor IMAP.")