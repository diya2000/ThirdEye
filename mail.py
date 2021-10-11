import smtplib

def sendEmail(receiver,subject,message):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login("email_address","password")
    server.sendmail("emailaddress",receiver,message)
    
    print("succesful")

#sendEmail() enter your email address, reciver's email, message