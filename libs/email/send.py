import os
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from ..path.utils.file import BaseName
from framework import FrameworkException
from email.mime.multipart import MIMEMultipart

def _global_email(mail:smtplib.SMTP, subject:str, body:str, from_email:str, to_email:str, cc_email:str=None, cco_email:str=None, files:list = None, mime_type:str="plain"):
    """Send an email (global configuration).

    Args:
        mail (smtplib.SMTP): smtplib.SMTP connection.
        subject (str): Email subject.
        body (str): Email body.
        from_email (str): Email from.
        to_email (str): Email to send.
        cc_email (str, optional): Email with cc. Defaults to None.
        cco_email (str, optional): Email with bcc. Defaults to None.
        files (list, optional): Files to send. Defaults to None.
        mime_type (str, optional): Type body (html, plain, ...). Defaults to "plain".

    Raises:
        FrameworkException: In case of error to send.
        Exception: _description_
    """
    try:
        message = MIMEMultipart()
        message['From'] = from_email
        message['To'] = (',').join(to_email.split(';'))
        if cc_email: 
            message['Cc'] = (',').join(cc_email.split(';')) 
        if cco_email: 
            message['Bcc'] = (',').join(cco_email.split(';'))
        message['Subject'] = subject
        message.attach(MIMEText(body, mime_type))
        if(files is not None):
            for key, file in enumerate(files):
                file_name = None
                if(isinstance(file, dict) and file.get("file_ubication")):
                    file_ubication = file['file_ubication']
                    if(file.get("file_name")):
                        file_name = file['file_name']
                elif(isinstance(file, str)):
                    file_ubication = file
                if(file is not None and os.path.exists(file_ubication)):
                    file_name = 'file (%s).%s' %(key, file_ubication.split('.')[-1]) if not file_name else file_name
                    with open(file_ubication, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename={file_name}')
                    message.attach(part)
        list_emails = f'{message["To"]}, {message["Cc"]}, {message["Bcc"]}'.replace(" ","").split(",")
        list_emails = list(filter(lambda x: x not in "None", list_emails))
        mail.sendmail(from_email, list_emails, message.as_string())
    except (smtplib.SMTPException, Exception) as e:
        raise FrameworkException("An error ocurred when send the email: " % e)
    
def onlyText(mail:smtplib.SMTP, subject:str, body:str, from_email:str, to_email:str, cc_email:str=None, cco_email:str=None, mime_type:str="plain"):
    """Send an email with only text.

    Args:
        mail (smtplib.SMTP): smtplib.SMTP connection.
        subject (str): Email subject.
        body (str): Email body.
        from_email (str): Email from.
        to_email (str): Email to send.
        cc_email (str, optional): Email with cc. Defaults to None.
        cco_email (str, optional): Email with bcc. Defaults to None.
        mime_type (str, optional): Type body (html, plain, ...). Defaults to "plain".
    """
    _global_email(mail, subject, body, from_email, to_email, cc_email, cco_email, mime_type=mime_type)
    
def withFiles(mail:smtplib.SMTP, subject:str, body:str, from_email:str, to_email:str, files:list|str, cc_email:str="", cco_email:str="", mime_type:str="plain"):
    """Send an email with text and files.

    Args:
        mail (smtplib.SMTP): smtplib.SMTP connection.
        subject (str): Email subject.
        body (str): Email body.
        from_email (str): Email from.
        to_email (str): Email to send.
        files (list|str, optional): Files to send.
        cc_email (str, optional): Email with cc. Defaults to None.
        cco_email (str, optional): Email with bcc. Defaults to None.
        mime_type (str, optional): Type body (html, plain, ...). Defaults to "plain".
    """
    if isinstance(files, str):
        files = [{"file_ubication":files, "file_name":BaseName(files)}]
    _global_email(mail, subject, body, from_email, to_email, cc_email, cco_email, files, mime_type)