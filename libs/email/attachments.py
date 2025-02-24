import email
import email.message
import poplib
import imaplib
import mimetypes
from typing import Callable
from ..path.loader import env

#Filters with imaplib.IMAP4
FROM = '(FROM "%s")'
SINCE_BEFORE='(SINCE "%s" BEFORE "%s")'
SUBJECT='(SUBJECT "%s")'.encode("ASCII", 'ignore').decode('ASCII')

def downloadAttachments(m:imaplib.IMAP4|poplib.POP3, filter:str="", select:str = "inbox", outputdir:str = env("OUTPUT_DIR"), filter_case_pop3:Callable[[email.message.EmailMessage],bool]=None):
    """Download attachments from emails based on a filter.

    Args:
        m (imaplib.IMAP4 | poplib.POP3): imaplib.IMAP4 | poplib.POP3 connection.
        filter (str, optional): Search filter to emails (recommended use variable FROM|SINCE_BEFORE|SUBJECT if m is instance of imaplib.IMAP4). Defaults to ""
        select (str, optional): Folder to select. Defaults to "inbox".
        outputdir (str, optional): Output directory to save file attachments. Defaults to env("OUTPUT_DIR").
        filter_case_pop3 (Callable[[email.message.EmailMessage],bool], optional): Function to filter emails with poplib.POP3. Defaults to None.

    Raises:
        ValueError: If m is not imaplib.IMAP4 | poplib.POP3. Also if filter_case_pop3 is not callable and m is poplib.POP3.
    """
    if isinstance(m, imaplib.IMAP4):
        m.select(select)
        _, msgs = m.search(None, filter)
        email_ids = msgs[0].split()
    elif isinstance(m, poplib.POP3):
        if not isinstance(filter_case_pop3, Callable):
            raise ValueError(f"{filter_case_pop3} must be provided for POP3")
        email_ids = _filter_emails_pop3(m, filter_case_pop3)
    else:
        raise ValueError("Unsupported mail server connection type")
    for email_id in email_ids:
        _download_attachments_in_email(m, email_id, outputdir)
    

def _filter_emails_pop3(m:poplib.POP3, filter_func:Callable):
    """Filter emails for poplib.POP3 connection.

    Args:
        m (poplib.POP3): poplib.POP3 connection.
        filter_func (Callable): Function to filter emails.
    """
    email_ids = []
    for i in range(1, len(m.list()[1]) + 1):
        _, lines, _ = m.retr(i)
        email_body = b'\n'.join(lines)
        mail = email.message_from_bytes(email_body)
        if filter_func(mail):
            email_ids.append(i)
    return email_ids

def _download_attachments_in_email(m:imaplib.IMAP4|poplib.POP3, emailid:bytes, outputdir:str):
    """Download files from email address.

    Args:
        m (imaplib.IMAP4|poplib.POP3): imaplib.IMAP4|poplib.POP3 connection.
        emailid (bytes): The ID of the email to fetch attachments from.
        outputdir (str): Directory to save file attachments.
    """
    if isinstance(m, imaplib.IMAP4):
        _, data = m.fetch(emailid, "(BODY.PEEK[])")
        email_body = data[0][1]
    elif isinstance(m, poplib.POP3):
        _, lines, _ = m.retr(emailid)
        email_body = b'\n'.join(lines)
    mail = email.message_from_bytes(email_body)
    if mail.get_content_maintype() != 'multipart':
        return
    for part in mail.walk():
        if part.get_content_type() != 'multipart' and part.get('Content-Disposition') is not None:
            ext = mimetypes.guess_extension(part.get_content_type())
            filename = "%s.mail%s" %(part.get_filename(), ext)
            with open(outputdir + "/" + filename, "wb") as f:
                f.write(part.get_payload(decode=True))