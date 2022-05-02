import datetime
import email
import distutils
import imap_tools
from imap_tools import MailBox, A
import configparser
import time

config = configparser.ConfigParser()
config.sections()
config.read('config.ini')
config.sections()

# Global vars
min_size = int(int(config['DEFAULT']['min_size_MB']) * 1e6)
email_age_days = int(config['DEFAULT']['email_age_days'])
standard_folder = config['DEFAULT']['standard_folder']
test_mode = distutils.util.strtobool(config['DEFAULT']['test_mode'])
server = config['mailserver']['server']
user = config['mailserver']['user']
password = config['mailserver']['password']

max_date = datetime.date.today() - datetime.timedelta(days=email_age_days)

print("Searching for messages older than", max_date, "and larger than {:.2f}MB".format(min_size/1e6), "in folder", standard_folder, "...")
tic = time.time()

with MailBox(server).login(user, password) as mailbox:
    folder_list = mailbox.folder.list()
    mailbox.folder.set(standard_folder.replace('"', ''))
    # msg_uids = mailbox.uids(A(size_gt=min_size, date_lt=max_date))
    progress = 0
    processed = 1
    while processed:
        processed = 0
        msgs = mailbox.fetch(A(size_gt=min_size, date_lt=max_date), limit=1)
        for msg in msgs:
            processed = 1
            progress += 1
            print("Progress: ", progress, ", Time: ", int(time.time() - tic), ", UID: ", msg.uid, ", Sbj:", msg.subject, "; Date: ", msg.date, "; Size: {:.2f}MB".format(msg.size_rfc822 / 1e6))
            if not test_mode:
                new_message = email.message.EmailMessage()
                new_message["From"] = msg.from_
                new_message["To"] = msg.to
                new_message["Subject"] = msg.subject.replace('\r\n', '')
                Str = "This message contained followed attachments that have been stripped out:\r\n"
                for att in msg.attachments:
                    Str += "F: " + att.filename + "; S: " + str(att.size) + "B\r\n"
                Str += "Original message is:\r\n****************************\r\n\r\n" + msg.text
                new_message.set_payload(Str)
                # Fix special characters by setting the same encoding we'll use later to encode the message
                new_message.set_charset(email.charset.Charset("utf-8"))
                encoded_message = str(new_message).encode("utf-8")
                mailbox.client.append(standard_folder, imap_tools.MailMessageFlags.SEEN, msg.date, encoded_message)
                mailbox.move(msg.uid, '[Gmail]/Bin')
