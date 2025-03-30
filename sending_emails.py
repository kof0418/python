import smtplib
import getpass

smtp_obj = smtplib.SMTP("smtp.gmail.com", 587)
smtp_obj.ehlo()
smtp_obj.starttls()

# email = input("Enter your email: ")
# password = getpass.getpass("Enter your passwd: ")
email = "pythontesting.taiwan@gmail.com"
password = "XXXXXXXXXXXXXXXXXX"
smtp_obj.login(email, password)
# print(smtp.obj.login(email,password))

from_address = email
to_address = email
subject = input("Enter subject: ")
message = input("Enter message: ")
full_message = "Subject: " + subject + "\n" + message

print(smtp_obj.sendmail(from_address, to_address, full_message))
smtp_obj.quit()
