import sys
pieces_number = 15

class Artwork:
    categories = {}
    def __init__(self, artID,category,isAIMade):
        if self.category in artwork.categories:
            categories[self.category][self.artID] = self.isAIMade
        else:
            categories[self.category] = {self.artID: (self.isAIMade)}
    @classmethod
    def isCorrectGuess(cls, category,artID, isAIMade):
        try:
            correct_guess = cls.categories[category][artID]
        except:
            print("you are trying to access a non existing entry in the guess")
        return (correct_guess == isAImade)
        
class Player:
    def __init__(self, name):
        self.name = name
        self.place = ""
        self.guesses = {}
    def guess(self, category, artID, isRealPainter):
        #TODO implements a guess method that updates some sort of tracker
        action = ""
        if category != self.place: 
            #in this case we change rooms
            #closes the door in the game
            action = f"closeDoors:{self.place}"
            #changes the current place to the new room
            self.place = category
            #create a new entry to store the guesses
            self.guesses[category] = {key: None for key in artwork.categories[category].keys()}
            #registers the first guess
            self.guesses[category][artID] = artwork.isCorrectGuess(category,artID,isRealPainter)
        else:
            self.guesses[category][artID] = artwork.isCorrectGuess(category,artID,isRealPainter)
            #we check if there are more paintings left to be checked
            if None not in self.guesses[category].values():
                action = f"openDoors:{self.place}"
                updateDB()
        sys.stdout.write(action)
    def updateDB():
        #sends the current information in guesses in order to update the database
        pass
    def ends_expedition(self):
        #TODO implements a method that handles the end of the expedition
        #can you finish the game-> yes/no 
        #show statistics
        pass
    if __name__ == __main__:
        if sys.argv[1] == "-p":
            player = Player(sys.argv[2])
        elif sys.argv[1] == "-g":
            player.guess(argv[2],argv[3],argv[4])
            
            
            
        
   
