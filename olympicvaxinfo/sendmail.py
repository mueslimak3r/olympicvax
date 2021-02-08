import os


def sendmail(subject, body):
  os.system('echo "' + body + '" | mailx -r cam@cameronlambert.com -s ' + subject + 'xntl5lpu1@lists.mailjet.com')