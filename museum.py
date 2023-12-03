import sys
pieces_number = 15

class Artwork:
    categories = {}
    def __init__(self, artID,category,isAIMade):
        if category in Artwork.categories:
            Artwork.categories[self.category][self.artID] = self.isAIMade
        else:
            Artwork.categories[self.category] = {self.artID: (self.isAIMade)}
    @classmethod
    def isCorrectGuess(cls, category,artID, isAIMade):
        try:
            correct_guess = cls.categories[category][artID]
        except:
            print("you are trying to access a non existing entry in the guess")
        return (correct_guess == isAIMade)
        
class Player:
    def __init__(self, name):
        self.name = name
        self.place = ""
        self.guesses = {}
        print(name)
    def guess(self, category, artID, isRealPainter):
        #TODO implements a guess method that updates some sort of tracker
        action = ""
        if category != self.place: 
            #in this case we change rooms
            #closes the door in the game
            action = f"closeDoors\n{self.place}"
            #changes the current place to the new room
            self.place = category
            #create a new entry to store the guesses
            self.guesses[category] = {key: None for key in Artwork.categories[category].keys()}
            #registers the first guess
            self.guesses[category][artID] = Artwork.isCorrectGuess(category,artID,isRealPainter)
            print(action)
        else:
            self.guesses[category][artID] = Artwork.isCorrectGuess(category,artID,isRealPainter)
            #we check if there are more paintings left to be checked
            if None not in self.guesses[category].values():
                action = f"openDoors\n{self.place}"
                self.updateDB()
                print(action)
    def updateDB():
        #sends the current information in guesses in order to update the database
        pass
    def ends_expedition(self):
        #TODO implements a method that handles the end of the expedition
        #can you finish the game-> yes/no 
        #show statistics
        pass
   
#logindata:
#gmail: krolljesse0@gmail.com
#password: SDproject123456!
#pass: gfsnhyjgslbmrrtw
class Statistic:
    smtp_port = 587                 # Standard secure SMTP port
    smtp_server = "smtp.gmail.com"  # Google SMTP Server

    # Set up the email lists
    email_from = "krolljesse0@gmail.com"
    email_list = ["jessekroll2@gmail.com"]# possible to add more emails
    
    pswd = "gfsnhyjgslbmrrtw" 

    subject = "Score for GuessAI"

    def send_emails(email_list, playername,filename):

        for person in email_list:

            # Make the body of the email
            body = f"""
            Hey {playername},
            here are your score attached in a file. 
            You can open the file and see how well you performed.
            All the best, 
            your GuessAI team
            """

            # make a MIME object to define parts of the email
            msg = MIMEMultipart()
            msg['From'] = Statistic.email_from
            msg['To'] = person
            msg['Subject'] = Statistic.subject

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
            TIE_server = smtplib.SMTP(Statistic.smtp_server, Statistic.smtp_port)
            TIE_server.starttls()
            TIE_server.login(Statistic.email_from, Statistic.pswd)
            #print("Succesfully connected to server")
            


            # Send emails to "person" as list is iterated
            #print(f"Sending email to: {person}...")
            TIE_server.sendmail(Statistic.email_from, person, text)
            #print(f"Email sent to: {person}")
            

        # Close the port
        TIE_server.quit()


    # Run the function
#Statistic.send_emails(Statistic.email_list, "Leon","C:/Users/49173/Downloads/Quiz3.pdf" )


if __name__ == '__main__':
    if sys.argv[1] == "-p":
        player = Player(sys.argv[2])
    elif sys.argv[1] == "-g":
        player.guess(sys.argv[2],sys.argv[3],bool(sys.argv[4]))