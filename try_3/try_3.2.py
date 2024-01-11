    # import required libraries
import imaplib
import email
from email.header import decode_header
import webbrowser
import os

def print_emails(year,month,date):
    # use your email id here
    username = '21f1007026@ds.study.iitm.ac.in'
    from app_pwd import pwd
    password = pwd

    # create a imap object
    imap = imaplib.IMAP4_SSL("imap.gmail.com")

    # login
    result = imap.login(username, password)

    # Use "[Gmail]/Sent Mails" for fetching
    # mails from Sent Mails. 
    imap.select('"[Gmail]/All Mail"', 
    readonly = True) 

    # typ, msgnums = imap.search(None, 'FROM', '"LDJ"')
    import datetime

    # specify date range
    start_date = datetime.date(year, month, date)
    
    # start_date = datetime.date(2024, 1, 10)
    # the above date is in YYYY, M, D format
    end_date = start_date + datetime.timedelta(1)

    # format dates for IMAP
    start_str = start_date.strftime("%d-%b-%Y")
    end_str = end_date.strftime("%d-%b-%Y")

    # search for emails between start date and end date
    res, messages = imap.search(None, '(SINCE "{}" BEFORE "{}")'.format(start_str, end_str))
    messages = messages[0].split()

    # take it from last
    latest = int(messages[-1])

    # take it from start
    oldest = int(messages[0])



    for i in range(oldest, latest+1):
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                print("#########################################################################")
                print(msg["From"])
                print(msg["Date"])
                if msg["From"]=="meetings-noreply@google.com":
                    print(msg["Date"])
                    print(msg["Subject"])
                    for part in msg.walk():
                        if part.get_content_type() == "text / plain":
                            body = part.get_payload(decode = True)
                            print(f'Body: {body.decode("UTF-8")}', )

print_emails(2024,1,10)
# print_emails(2023,11,10)