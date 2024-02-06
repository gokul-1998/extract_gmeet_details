    # import required libraries
import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup  # Make sure to install BeautifulSoup using: pip install beautifulsoup4

def extract_gsheet_link(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    link = soup.find('a', href=True)
    if link:
        return link['href']
    return None

import webbrowser
import os

def print_gsheet(gmeet_link,date, month, year,no_of_days=1):
    # use your email id here
    username = 'mentor-admin@study.iitm.ac.in'
    # username="21f1007026@ds.study.iitm.ac.in"
    from app_pwd import pwd
    password = pwd

    # create a imap object
    imap = imaplib.IMAP4_SSL("imap.gmail.com")

    # login
    result = imap.login(username, password)
    print("login result",result)
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
    messages = messages[0].split(b' ')

    for mail in messages:
        # print("inside mail")
        
        _, msg = imap.fetch(mail, "(BODY[])")
        email_message = email.message_from_bytes(msg[0][1])
        print(email_message["From"])
        if email_message["From"] == "meetings-noreply@google.com":
            # print(f'From: {email_message["From"]} {email_message["Date"]}')
            print(f'Subject: {email_message["Subject"]}')
            # print(f'Content-Type: {email_message.get_content_type()}')
            print(email_message)
            # print()
            # print(extract_gsheet_link(email_message))
            
            # break
            
            # if the email message is multipart
            if email_message.is_multipart():
                for part in email_message.get_payload():
                    # if the content type is text/html
                    print("###############333",part.get_content_type())
                    if part.get_content_type() == "text/html":
                        body = part.get_payload(decode=True)
                        gsheet_link = extract_gsheet_link(body)
                        print("@@@@@@@@@@@@@@@",gsheet_link)
                        if gsheet_link :
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
print_gsheet(gmeet_link,4, 2, 2024)