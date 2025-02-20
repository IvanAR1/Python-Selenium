import os
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from ..path.path_utils import BaseName

def globalEmail(mail:smtplib.SMTP, subject:str, body:str, from_email:str, to_email:str, cc_email:str=None, cco_email:str=None, files:list = None):
    try:
        message = MIMEMultipart()
        message['From'] = from_email
        message['To'] = (',').join(to_email.split(';'))
        message['CC'] = (',').join(cc_email.split(';')) if cc_email is not None else None
        message['CCO'] = (',').join(cco_email.split(';')) if cco_email is not None else None
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
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
        mail.sendmail(from_email, to_email, message.as_string())
    except smtplib.SMTPException as e:
        raise Exception("Error al enviar el correo: %s" % e)
    except Exception as e:
        raise Exception("Error al enviar el correo: %s" %e)
    
def onlyText(mail:smtplib.SMTP, subject:str, body:str, from_email:str, to_email:str, cc_email:str=None, cco_email:str=None):
    globalEmail(mail, subject, body, from_email, to_email, cc_email, cco_email)
    
def withFiles(mail:smtplib.SMTP, subject:str, body:str, from_email:str, to_email:str, files:list|str, cc_email:str="", cco_email:str=""):
    if isinstance(files, str):
        files = [{"file_ubication":files, "file_name":BaseName(files)}]
    globalEmail(mail, subject, body, from_email, to_email, cc_email, cco_email, files)