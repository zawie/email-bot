import smtplib
import time 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import csv 

#Constants
SENDER_LOGIN = 'dev.riceapps@gmail.com'
SENDER_ALIAS = 'RiceApps<dev.riceapps@gmail.com>'
PASSWORD = ''
CC = ['Adam.Zawierucha@rice.edu'] #'Cloris.Cai@rice.edu'
DELAY = 1

def createSession():
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(SENDER_LOGIN, PASSWORD) #login with mail_id and password
    return session

def createMessage(receiver_address, orgName):
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = SENDER_ALIAS
    message['To'] = receiver_address
    message['Cc'] = ",".join(CC)
    message['Subject'] = f'RiceApps & {orgName} Collaboration Opportunity'   #The subject line

    mail_content = f"""Hello,

We are Adam and Cloris, the chairs of RiceApps (https://riceapps.org), a student organization at Rice University dedicated to building digital solutions for social good. We are reaching out to see if your organization has a problem we can solve with custom software.

In the past, we have built tools that increased productivity and efficiency of local non-profit organizations. Here are some projects we have built this past year:
    - A mobile application for Second Servings to connect surplus food to organizations that can distribute it. 
    - A web application to help Hives for Heroes match veterans to bee keeping mentors to facilitate honey bee conservation, suicide prevention, and a healthy transition from service.
    - An automated matching solution for the Rice Career Center to efficiently match students to externship opportunities.
    - A chatbot with the Patient Discharge Initiative to connect patients to necessary resources. 

We are not seeking compensation — we are eager to make an impact in your organization and the local community. 

Is there an opportunity for us to solve a problem for your organizaton? If not, could you kindly refer us to an organization we can assist?

Best,
Cloris Cai & Adam Zawierucha
Chairs of RiceApps
"""
    message.attach(MIMEText(mail_content, 'plain'))

    return message

def sendMail(session, reciever, message):
    text = message.as_string()
    session.sendmail(SENDER_LOGIN, reciever, text)

#Count how many people are being sent
count = 0
with open('recipients.csv', newline='') as csvfile:
 count = sum(1 for _ in csv.reader(csvfile, delimiter=',', quotechar='|'))

#Ask for confirmation
print(f'Are you sure you want to run this email bot? 📫\n Recipient count: {count}\n Delay: {DELAY}\n Sender Alias: {SENDER_ALIAS}\n CC: {", ".join(CC)}\n(y/n)')
confirmation = input() == 'y'

if (confirmation):
    #Create session
    session = createSession()

    print("Sending Emails... 📬")
    i = 0
    with open('recipients.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        i += 1
        for (orgName, reciever) in spamreader:
            message = createMessage(reciever, orgName)
            reciepients = [reciever] + CC
            sendMail(session, reciepients, message)
            print(f' ✔️ Message Sent to "{orgName}" ({reciever}).')
            time.sleep(DELAY)
    print(f"Done! Sent {i} emails. 📭 ")
    #End session
    session.quit()
    print("Session ended.")
else:
    print("Program exited.")
