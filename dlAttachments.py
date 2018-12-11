# Referenced http://stackoverflow.com/questions/348630/how-can-i-download-all-emails-with-attachments-from-gmail
# Make sure you have IMAP enabled in your gmail settings.
# See / create issues on github.com/bmitchinson/raspberry-pi-photo-frame

import sys
import imaplib
import email
import email.header
import datetime
import os

# All pictures downloaded to "/Attachments" by default
detach_dir = '.'
if 'Attachments' not in os.listdir(detach_dir):
    os.mkdir('Attachments')

# Replace *username* and *password*
EMAIL_ACCOUNT = "*USERNAME*@gmail.com"
EMAIL_PASSWORD = "*PASSWORD*"
# Use a dedicated folder if desired, otherwise leave as "INBOX" to search inbox
EMAIL_FOLDER = "INBOX"

try:
    imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
    typ, accountDetails = imapSession.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    if typ != 'OK':
        print('Not able to sign in!')
        raise
    imapSession.select('INBOX')
    typ, data = imapSession.search(None, 'ALL')
    if typ != 'OK':
        print('Error searching Inbox.')
        raise
    # Iterating over all emails
    for msgId in data[0].split():
        typ, messageParts = imapSession.fetch(msgId, '(RFC822)')
        if typ != 'OK':
            print('Error fetching mail.')
            raise

        emailBody = messageParts[0][1]
        mail = email.message_from_bytes(emailBody)
        for part in mail.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            fileName = part.get_filename()

            if bool(fileName):
                filePath = os.path.join(detach_dir, 'Attachments', fileName)
                if not os.path.isfile(filePath) :
                    print(fileName)
                    fp = open(filePath, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
    imapSession.close()
    imapSession.logout()
    
except:
    print('Not able to download all attachments.')
