import os

def sendmail(subject, body):
    command = 'echo "' + '<a href="[[UNSUB_LINK_LOCALE]]">click here to unsubscribe</a>' + '\n' + body + '" | mailx -r jeffcovax@cameronlambert.com -s "' + subject + '" xntl5lpu1@lists.mailjet.com'
    print("sending mail to mailing list")
    os.system(command)
