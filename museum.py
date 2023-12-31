import sys
import smtplib
import artwork_database as adb
from json import dump, load
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

pieces_number = 15

class Artwork:
    
    categories = {}
    
    def __init__(self, artID,category, humanOrAI):
        isHumanMade = True if humanOrAI == "Human" else False
        if category in Artwork.categories:
            Artwork.categories[category][artID] = isHumanMade
        else:
            Artwork.categories[category] = {artID: (isHumanMade)}
            
    @classmethod
    def isCorrectGuess(cls, category,artID, isHumanMade):
        try:
            correct_guess = cls.categories[category][artID]
        except:
            print("you are trying to access a non existing entry in the guess")
        isCorrectGuess = (correct_guess == isHumanMade)
        sys.stdout.write(str(isCorrectGuess) + " ")
        return isCorrectGuess
    
    @classmethod
    def from_file(cls):
        cls.categories = load(open("artworks.txt"))
        
    @classmethod
    def save_to_file(cls):
        dump(cls.categories, open("artworks.txt", "w"))
        
class Player:
    
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.place = ""
        self.guesses = {}

    @classmethod
    def from_file(cls):
        player = cls.__new__(cls)
        player_file = open("player_info.txt", "r")
        firstline = player_file.readline()
        player.name, player.email = firstline.split()
        player.place = player_file.readline()
        try:
            player.guesses = load(open("player_guesses.txt"))
        except:
            player.guesses = {}
        return player
        
    def guess(self, category, artID, isRealPainter):
        #TODO implements a guess method that updates some sort of tracker
        action = ""
        if category != self.place: 
            #in this case we change rooms
            #closes the door in the game
            action = f"closeDoors {category}"
            #changes the current place to the new room
            self.place = category
            #create a new entry to store the guesses
            self.guesses[category] = {key: None for key in Artwork.categories[category].keys()}
            #registers the first guess
            self.guesses[category][artID] = Artwork.isCorrectGuess(category,artID,isRealPainter)
        else:
            self.guesses[category][artID] = Artwork.isCorrectGuess(category,artID,isRealPainter)
            #we check if there are more paintings left to be checked
            if None not in self.guesses[category].values():
                action = f"openDoors {category}"
        return action
    
    def save_to_file(self, player_info = False, guess_info = False):
        if player_info:
            message = self.name + " " + self.email + "\n" + self.place
            file = open("player_info.txt", "w")
            file.write(message)
            file.close()
        if guess_info:
            dump(self.guesses, open("player_guesses.txt","w"))
            
    def send_email(self, files : list):
        
        smtp_port= 587# Standard secure SMTP port
        smtp_server = "smtp.gmail.com" # Google SMTP Server
        # Set up the email lists
        email_from = "krolljesse0@gmail.com"
        
        pswd = "gfsnhyjgslbmrrtw" 

        subject = "Test-Score for GuessAI"

        # Make the body of the email
        body = f"""
        Hey {self.name},
        test
        here are your score attached in a file. 
        You can open the file and see how well you performed.
        All the best, 
        your GuessAI team
        """

        # make a MIME object to define parts of the email
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = self.email
        msg['Subject'] = subject

        # Attach the body of the message
        msg.attach(MIMEText(body, 'plain'))

        for file in files:
            # Open the file in python as a binary
            attachment = open(file, 'rb')  # r for read and b for binary
    
            # Encode as base 64
            attachment_package = MIMEBase('application', 'octet-stream')
            attachment_package.set_payload((attachment).read())
            encoders.encode_base64(attachment_package)
            attachment_package.add_header('Content-Disposition', "attachment; filename= " + file)
            msg.attach(attachment_package)

        # Cast as string
        text = msg.as_string()

        #Connect with the server
        #print("Connecting to server...")
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls()
        TIE_server.login(email_from, pswd)
        #print("Succesfully connected to server")
        


        # Send emails to "person" as list is iterated
        #print(f"Sending email to: {person}...")
        TIE_server.sendmail(email_from, self.name, text)
        #print(f"Email sent to: {person}")
            

        # Close the port
        TIE_server.quit()

        # Run the function
            
        
   
#logindata:
#gmail: krolljesse0@gmail.com
#password: SDproject123456!
#pass: gfsnhyjgslbmrrtw


# stat_instance = Statistic("Example")
# stat_instance.execute()

if __name__ == '__main__':
    if sys.argv[1] == "-p":
        if os.path.exists("player_guesses.txt"):
            os.remove("player_guesses.txt")
        player = Player(sys.argv[2],sys.argv[3])
        player.save_to_file(player_info = True)
        
        db = adb.Database()
        db.create_db()
        db.begin_game_name(player.name)
        db.commit()
        artworks = db.give_images()
        print(artworks)
        for artwork in artworks:
            artID, humanOrAI, room = artwork
            Artwork(artID,room,humanOrAI)
        Artwork.save_to_file()
        db.__exit__()
        
    elif sys.argv[1] == "-g":
        player = Player.from_file()
        Artwork.from_file()
        guess_result = player.guess(sys.argv[2],sys.argv[3],eval(sys.argv[4]))
        player.save_to_file(guess_info = True)
        if guess_result != "":
            action, room = guess_result.split()
            sys.stdout.write(action)
            if action == "closeDoors":
                player.room = room
                player.save_to_file(player_info = True)
            if action == 'openDoors':
                db = adb.Database()
                db.update_DB(player.name, player.guesses[player.place].items())
                player.place = ""
                player.save_to_file(player_info = True)
                db.commit()
                db.__exit__()
                
    elif sys.argv[1] == "-e":
        player = Player.from_file()
        print(player.place)
        if player.place == "":
            Artwork.from_file()
            db = adb.Database()
            db.updateScore(player.name)
            db.commit()
            db.pie_chart(player.name)
            db.score_numPlayer_total()
            list_of_files = ['score_histogram_total.png', 'pie_chart.png']
            for room in player.guesses.keys():
                db.score_numPlayer_room(room)
                list_of_files.append(f'score_histogram_{room}.png')
            player.send_email(list_of_files)
            #delete files -> not sure if this works:
            if os.path.exists("score_histogram_total.png"):
                os.remove("score_histogram_total.png")
            if os.path.exists("pie_chart.png"):
                os.remove("pie_chart.png")
            db.__exit__()
            print("true")
        else:
            print("false")
