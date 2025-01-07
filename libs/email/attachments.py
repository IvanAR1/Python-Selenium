import email, mimetypes, imaplib
from framework import env

FROM = '(FROM "%s")'
SINCE_BEFORE='(SINCE "%s" BEFORE "%s")'
SUBJECT='(SUBJECT "%s")'.encode("ASCII", 'ignore').decode('ASCII')

def downloadAttachmentsInEmail(m:imaplib.IMAP4, emailid:bytes, outputdir):
    resp, data = m.fetch(emailid, "(BODY.PEEK[])")
    email_body = data[0][1]
    mail = email.message_from_bytes(email_body)
    if mail.get_content_maintype() != 'multipart':
        return
    for part in mail.walk():
        if part.get_content_maintype() != 'multipart' and part.get('Content-Disposition') is not None:
            ext = mimetypes.guess_extension(part.get_content_type())
            filename = "%s.mail%s" %(part.get_filename(), ext)
            open(outputdir + '/' + filename, 'wb').write(part.get_payload(decode=True))

def downloadAttachments(m:imaplib.IMAP4, filter:str, select:str = "inbox", outputdir:str = env("OUTPUT_DIR")):
    m.select(select)
    search = filter
    typ, msgs = m.search(None, search)
    msgs = msgs[0].split()
    for emailid in msgs:
        downloadAttachmentsInEmail(m, emailid, outputdir)