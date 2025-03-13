import ssl
import poplib
import socket
import smtplib
import imaplib
from libs.path.loader import env
from framework import FrameworkException

def smtp(
    host: str = env("SMTP_HOST"),
    port: int = env("SMTP_PORT"),
    user: str = env("MAIL_USER"),
    pwd: str = env("MAIL_PWD"),
    ssl_context:ssl.SSLContext=ssl.create_default_context(),
    timeout: float = 20,
) -> smtplib.SMTP:
    """Generate a smtplib.SMTP connection.

    Args:
            
        port (int, optional): Email provider port. Defaults to env("SMTP_PORT").
        user (str, optional): Email address. Defaults to env("MAIL_USER").
        pwd (str, optional): Email address password. Defaults to env("MAIL_PWD").
        ssl_context (ssl.SSLContext, optional): SSL in case to applied. Defaults to ssl.create_default_context().
        timeout (float, optional): Timeout to connect. Defaults to 20.

    Raises:
        FrameworkException: In case an error occurs while trying to connect to SMTP server.

    Returns:
        smptlib.SMTP: SMTP connection.
    """
    try:
        mail = smtplib.SMTP(host=host, port=port, timeout=timeout)
        mail.ehlo()
        mail.starttls(context=ssl_context)
        mail.ehlo()
        mail.login(user=user, password=pwd)
        return mail
    except (
        smtplib.SMTPException,
        TimeoutError,
        ConnectionRefusedError,
        Exception,
    ) as e:
        raise FrameworkException("An error ocurred when trying to connect to SMTP server: %s" % e)


def imap(
    host: str = env("IMAP_HOST"),
    port: int = env("IMAP_PORT"),
    user: str = env("MAIL_USER"),
    pwd: str = env("MAIL_PWD"),
    ssl_context:ssl.SSLContext=ssl.create_default_context(),
    timeout: float = 20
)->imaplib.IMAP4:
    """Generate a imaplib.IMAP4 connection.

    Args:
        host (str, optional): Email provider host. Defaults to env("IMAP_HOST").
        port (int, optional): Email provider port. Defaults to env("IMAP_PORT").
        user (str, optional): Email address. Defaults to env("MAIL_USER").
        pwd (str, optional): Email address password. Defaults to env("MAIL_PWD").
        ssl_context (ssl.SSLContext, optional): SSL in case to applied. Defaults to ssl.create_default_context().
        timeout (float, optional): Timeout to connect. Defaults to 20.

    Raises:
        FrameworkException: In case an error occurs while trying to connect to IMAP server.

    Returns:
        imaplib.IMAP4: IMAP4 connection.
    """
    try:
        socket.setdefaulttimeout(timeout)
        m = imaplib.IMAP4(host=host, port=port, timeout=20)
        m.ehlo()
        m.starttls(ssl_context=ssl_context)
        m.ehlo()
        m.login(user=user, password=pwd)
        return m
    except (
        imaplib.IMAP4_SSL.error,
        TimeoutError,
        ConnectionRefusedError,
        Exception,
    ) as e:
        raise FrameworkException("An error ocurred when trying to connect to IMAP server: %s" % e)


def pop(
    host: str = env("POP_HOST"),
    port: int = env("POP_PORT"),
    user: str = env("MAIL_USER"),
    pwd: str = env("MAIL_PWD"),
    ssl_context:ssl.SSLContext = ssl.create_default_context(),
    timeout: float = 20
):
    """Generate a poplib.POP3 connection.

    Args:
        host (str, optional): Email provider host. Defaults to env("POP_HOST").
        port (int, optional): Email provider port. Defaults to env("POP_PORT").
        user (str, optional): Email address. Defaults to env("MAIL_USER").
        pwd (str, optional): Email address password. Defaults to env("MAIL_PWD").
        ssl_context (ssl.SSLContext, optional): SSL in case to applied. Defaults to ssl.create_default_context().
        timeout (float, optional): Timeout to connect. Defaults to 20.

    Raises:
        FrameworkException: In case an error occurs while trying to connect to POP server.

    Returns:
        poplib.POP3: POP3 connection.
    """
    try:
        socket.setdefaulttimeout(timeout)
        pop = poplib.POP3(host=host, port=port)
        pop.stls(context=ssl_context)
        pop.user(user)
        pop.pass_(pwd)
        return pop
    except (TimeoutError, ConnectionRefusedError, Exception) as e:
        raise FrameworkException("An error ocurred when trying to connect to POP server: %s" % e)