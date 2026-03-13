import yagmail
import os
import datetime
date = datetime.date.today().strftime("%B %d, %Y")
path = 'Attendance'
os.chdir(path)
files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
newest = files[-1]
filename = newest
sub = "Attendance Report for " + str(date)
# mail information
# [IMPORTANT]: Update your email and app-specific password before running this feature.
email_user = "aafqlatif804@gmail.com"
email_pass = "password" # Use an app-specific password if using Gmail
receiver = "afaqlatif082@gmail.com"
body = "Please find the attached attendance report."

yag = yagmail.SMTP(email_user, email_pass)

# sent the mail
yag.send(
    to=receiver,
    subject=sub, # email subject
    contents=body,  # email body
    attachments= filename  # file attached
)
print("Email Sent!")
