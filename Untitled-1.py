import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
class Statistic:
    def __init__(self, name):
        self.smtp_port= 587# Standard secure SMTP port
        self.smtp_server = "smtp.gmail.com" # Google SMTP Server
        # Set up the email lists
        self.email_from = "krolljesse0@gmail.com"
        self.email_list = ["jessekroll2@gmail.com", "patricijadziuzaite@gmail.com"]
        self.pswd = "gfsnhyjgslbmrrtw" 

        self.subject = "Test-Score for GuessAI"

    def send_emails(self, email_list, playername,filename):

        for person in email_list:

            # Make the body of the email
            body = f"""
            Hey {playername},
            test
            here are your score attached in a file. 
            You can open the file and see how well you performed.
            All the best, 
            your GuessAI team
            """

            # make a MIME object to define parts of the email
            msg = MIMEMultipart()
            msg['From'] = self.email_from
            msg['To'] = person
            msg['Subject'] = self.subject

            # Attach the body of the message
            msg.attach(MIMEText(body, 'plain'))

            # Open the file in python as a binary
            attachment= open(filename, 'rb')  # r for read and b for binary

            # Encode as base 64
            attachment_package = MIMEBase('application', 'octet-stream')
            attachment_package.set_payload((attachment).read())
            encoders.encode_base64(attachment_package)
            attachment_package.add_header('Content-Disposition', "attachment; filename= " + filename)
            msg.attach(attachment_package)

            # Cast as string
            text = msg.as_string()

            #Connect with the server
            #print("Connecting to server...")
            TIE_server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            TIE_server.starttls()
            TIE_server.login(self.email_from, self.pswd)
            #print("Succesfully connected to server")
            


            # Send emails to "person" as list is iterated
            #print(f"Sending email to: {person}...")
            TIE_server.sendmail(self.email_from, person, text)
            #print(f"Email sent to: {person}")
            

        # Close the port
        TIE_server.quit()


        # Run the function
    def execute(self):
        self.send_emails(self.email_list, "Champion",r"C:\Users\49173\Desktop\Sd correct git\museum\room_1_2.png")


stat_instance = Statistic("Example")
stat_instance.execute()