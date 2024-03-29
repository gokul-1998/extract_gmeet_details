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

def print_gsheet(gmeet_link,date, month, year,no_of_days=1):
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
    end_date = start_date + datetime.timedelta(no_of_days)
    end_date=start_date
    print(start_date)
    print(end_date)
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
            
            
            # if the email message is multipart
            if email_message.is_multipart():
                for part in email_message.get_payload():
                    # if the content type is text/html
                    if part.get_content_type() == "text/html":
                        body = part.get_payload(decode=True)
                        gsheet_link = extract_gsheet_link(body)
                        if gsheet_link and gmeet_link in email_message["Subject"]:
                            print(f'date: {email_message["Date"]}')
                            
                            # to get indian time for the above
                            print(f'Date: {email.utils.parsedate_to_datetime(email_message["Date"]).astimezone().strftime("%d/%m/%Y %H:%M:%S")}')

                            print(f'Subject: {email_message["Subject"]}')
                            print(f'Google Sheets Link: {gsheet_link}')
                    # if the content type is text/csv
                    # elif part.get_content_type() == "text/csv":
                    #     open('attachment.csv', 'wb').write(part.get_payload(decode=True))
            # else:
            #     # if the email isn't multipart
            #     if email_message.get_content_type() == "text/html":
            #         body = email_message.get_payload(decode=True)
            #         gsheet_link = extract_gsheet_link(body)
            #         if gsheet_link:
            #             print(f'Google Sheets Link: {gsheet_link}')
                # elif email_message.get_content_type() == "text/csv":
                #     open('attachment.csv', 'wb').write(email_message.get_payload(decode=True))

    # close the connection and logout
    imap.logout()

# Call the function with the desired date
# print_gsheet(10, 1, 2024)

import calendar
import datetime


def get_month_start_date_and_end_date(year, month):
    """
    Returns the start date and end date of the month in the format
    (start_date, end_date) where both start_date and end_date are datetime.date objects
    """
    # get the first day of the month
    start_date = datetime.date(year, month, 21)
    # get the last day of the month
    end_date = start_date + datetime.timedelta(calendar.monthrange(year, month)[1] - 1)
    diff = end_date - start_date
    print(diff.days)
    return start_date.day,start_date.month,start_date.year, diff.days

gmeet_link="fsa-vtgo-atp"
print_gsheet(gmeet_link,*get_month_start_date_and_end_date(2024, 1))