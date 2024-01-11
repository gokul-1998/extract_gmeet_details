import os
import datetime
import email
import imaplib
from email.header import decode_header
from bs4 import BeautifulSoup  # Make sure to install BeautifulSoup using: pip install beautifulsoup4

def extract_gsheet_link(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    link = soup.find('a', href=True)
    if link:
        return link['href']
    return None

def print_gsheet(date, month, year):
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

        if email_message["From"] == "meetings-noreply@google.com":
            print(f'From: {email_message["From"]}')
            # if the email message is multipart
            if email_message.is_multipart():
                for part in email_message.get_payload():
                    # if the content type is text/html
                    if part.get_content_type() == "text/html":
                        body = part.get_payload(decode=True)
                        gsheet_link = extract_gsheet_link(body)
                        if gsheet_link:
                            print(f'Google Sheets Link: {gsheet_link}')
                    # if the content type is text/csv
                    elif part.get_content_type() == "text/csv":
                        open('attachment.csv', 'wb').write(part.get_payload(decode=True))
            else:
                # if the email isn't multipart
                if email_message.get_content_type() == "text/html":
                    body = email_message.get_payload(decode=True)
                    gsheet_link = extract_gsheet_link(body)
                    if gsheet_link:
                        print(f'Google Sheets Link: {gsheet_link}')
                elif email_message.get_content_type() == "text/csv":
                    open('attachment.csv', 'wb').write(email_message.get_payload(decode=True))

    # close the connection and logout
    imap.logout()

# Call the function with the desired date
print_gsheet(11, 1, 2024)
