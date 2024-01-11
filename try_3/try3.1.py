# import required libraries
import imaplib
import email
from email.header import decode_header
import webbrowser
import os

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
response, messages = imap.search(None, '(FROM "meetings-noreply@google.com")')

messages = messages[0].split()

# take it from last
latest = int(messages[-1])

# take it from start
oldest = int(messages[0])

for i in range(latest, latest-20, -1):
	# fetch
	res, msg = imap.fetch(str(i), "(RFC822)")
	
	for response in msg:
		if isinstance(response, tuple):
			msg = email.message_from_bytes(response[1])
            # print required information
			print("#########################################################################")
			print(msg["From"])
			if msg["From"]=="meetings-noreply@google.com":
				print(msg["Date"])
				
				print(msg["Subject"])
				for part in msg.walk():
					if part.get_content_type() == "text / plain":
                        # get text or plain data
						body = part.get_payload(decode = True)
						print(f'Body: {body.decode("UTF-8")}', )
