# Readme

Retrieve emails larger than a minimum amount of MB and older than a minimum amount of days and
substitute them with a replica without attachments.
Original messages are placed in the bin, so remember to delete them to free up account space.

Test mode will loop forever on the first email since the search is done one by one.

Run it on a fast internet connection as it has to download all mails and attachments

Strongly inspired from https://github.com/guido4000/Email-Attachment-Remover

# Usage

- Use Python 3
- Adjust config.sample, rename to config.ini
	- Set IMAP mailbox login configuration
		- for GMAIL you can create an app password (the name does't matter, use here just the password)
	- Decide the minimum size of email (MB) and minimum age (days)
	- Decide the folder, I tried INBOX (no quotes) and "[Gmail]/Sent Mail" (with quotes)  
	- Disable test mode when you are sure
- Run PyEmail.py

