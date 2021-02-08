import os


def sendmail(subject, body):
    command = 'echo "' + body + '" | mailx -r jeffcovax@cameronlambert.com -s "' + subject + '" xntl5lpu1@lists.mailjet.com'
    print(command)
    os.system(command)
