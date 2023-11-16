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
if __name__ == '__main__':
    if sys.argv[1] == "-p":
        player = Player(sys.argv[2])
    elif sys.argv[1] == "-g":
        player.guess(sys.argv[2],sys.argv[3],bool(sys.argv[4]))
            
            
        
   
