import os
import datetime
import email
import imaplib
from email.header import decode_header

def print_emails(year, month, date):
    # use your email id here
    username = '21f1007026@ds.study.iitm.ac.in'
    from app_pwd import pwd
    password = pwd

    # create an IMAP4 class with SSL 
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    # authenticate
    imap.login(username, password)

    # select the mailbox you want to delete in
    # if you want SPAM, use "INBOX.SPAM"
    imap.select('"[Gmail]/All Mail"', readonly = True)

    # specify date range
    start_date = datetime.date(year, month, date)
    end_date = start_date + datetime.timedelta(1)

    # format dates for IMAP
    start_str = start_date.strftime("%d-%b-%Y")
    end_str = end_date.strftime("%d-%b-%Y")

    # search for specific mail by sender
    res, messages = imap.search(None, '(SINCE "{}" BEFORE "{}")'.format(start_str, end_str))
    messages = messages[0].split(b' ')

    for mail in messages:
        _, msg = imap.fetch(mail, "(BODY[])")
        email_message = email.message_from_bytes(msg[0][1])
        # to get the from email id
        print("#########################################################################")
        if  email_message["From"]=="meetings-noreply@google.com":
            print(f'From: {email_message["From"]}')
            print(email_message)
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            # if the email message is multipart
            if email_message.is_multipart():
                for part in email_message.get_payload():
                    # if the content type is text/plain
                    # we extract it
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True)
                        print(f'Body: {body.decode("UTF-8")}')
                    if part.get_content_type() == "text/csv":
                        open('attachment.csv', 'wb').write(part.get_payload(decode=True))
            else:
                # if the email isn't multipart
                if email_message.get_content_type() == "text/plain":
                    body = email_message.get_payload(decode=True)
                    print(f'Body: {body.decode("UTF-8")}')
                if email_message.get_content_type() == "text/csv":
                    open('attachment.csv', 'wb').write(email_message.get_payload(decode=True))

    # close the connection and logout
    imap.logout()

print_emails(2024,1,10)
