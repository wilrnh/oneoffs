#!/usr/bin/env python
""" sends an email with the contents of a file as the body of the email 

Password best-practices:
    * use `read -s SMTP_PASSWORD; export SMTP_PASSWORD` to set the password
    * alternatively read the password from a file with `export SMTP_PASSWORD=$(cat mypasswdfile)`
    * setting the password via the --smtp-password parameter leaves it open to both your bash history, and process list
"""

import argparse
import socket
import os
import time
import smtplib
from email.mime.text import MIMEText

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("-f", "--file", required=True, help="file to read content from")
parser.add_argument("-t", "--to", required=True, help="where to send file content to")
parser.add_argument("-u", "--smtp-user", required=True, help="username used to login to smtp server. also the email used in the From: field")
parser.add_argument("-p", "--smtp-password", default=os.environ.get('SMTP_PASSWORD'), help="password used to login to smtp server. looks at SMTP_PASSWORD env var first. REQUIRED.")
parser.add_argument("-s", "--smtp-server", default='smtp.gmail.com:587', help="smtp server to send mail from")
args = parser.parse_args()

if not args.smtp_password:
    exit(parser.print_usage())

FP = open(args.file, 'rb')
MSG = MIMEText(FP.read())
FP.close()

MSG['Subject'] = '%s: %s at %s' % (socket.gethostname(), args.file, time.asctime())
MSG['From'] = args.smtp_user
MSG['To'] = args.to
print (args.smtp_password)
s = smtplib.SMTP(args.smtp_server)
s.ehlo()
s.starttls()
s.login(args.smtp_user, args.smtp_password)
s.sendmail(args.smtp_user, [args.to], MSG.as_string())
s.quit()
