# Import dependencies
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from people import *
from time import sleep
import csv

# Loop forever
while True:
    # Get the current time and parse out the hour
    current_time = datetime.now()
    current_hour = current_time.strftime("%H")
    ### THIS CAN BE CHANGED. It is when the email is sent.
    if(int(current_hour) == 17):
        # Open up the file creds.txt and extract the email and password
        with open('creds.txt') as f:
            first_line = f.readline()
        fromaddr = first_line.split(":")[0]
        password = first_line.split(":")[1]

        # Create an array to hold the different users
        users = []

        # Read the users.csv file and extract each user
        with open('users.csv') as file:
            reader = csv.reader(file)
            next(reader)
            # For each user in the file create a people object for them
            for name, age, zip, email in reader:
                users.append(people(name.strip(), age.strip(), zip.strip(), email.strip()))

        # For each user
        for person in users:
            # Get their email
            toaddr = person.getEmail()

            # This is the email object initialization
            msg = MIMEMultipart()
            # Who is the email from
            msg['From'] = fromaddr
            # Who is the email going to?
            msg['To'] = toaddr

            # Establish the subject and body of the email for the person. The brains of this occurs in the people class
            msg['Subject'] , body = person.makeEmail()
            # We use HTML to format the email so it looks all pretty
            msg.attach(MIMEText(body, 'html'))

            # Connect to the gmail email server
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            # Log in to the email server with the email and password from creds.txt
            server.login(fromaddr, password)
            text = msg.as_string()
            # Actual process of sending the mail occurs here
            server.sendmail(fromaddr, toaddr, text)
            # Quit the server connection
            server.quit()
            print("Email sent to: " + person.getName())
        # Delay for more than an hour to ensure we don't send too many emails
        sleep(3600)
    else:
        # If its not time to send an email then we should go ahead and wait five minuted to ensure we don't wreck the cpu
        sleep(300)