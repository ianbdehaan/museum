import numpy as np 
pieces_number = 15
class artwork:
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
        
        
class player:
    def __init__(self, name):
        self.name = name
        self.place = ""
        self.guesses = {}
    def guess(self, category, artID, isrealpainter):
        #TODO implements a guess method that updates some sort of tracker
        if category != self.place: 
            #in this case we change rooms
            #closes the door in the game
            closeDoors()
            #changes the current place to the new room
            self.place = category
            #create a new entry to store the guesses
            self.guesses[category] = {key: None for key in artwork.categories[category].keys}
            #registers the first guess
            self.guesses[category][artID] = artwork.isCorrectGuess(category,artID,isAIMade)
        else:
            #in this case we check if there are more paintings left to be checked
            openDoors()
            pass
        pass
    #do opendoors and closedoors
    def change_place(self, new_place):
        #TODO implements a method that updated the place and saves the progress    
        if 
        #check if you can change place
        #update db with new guesses 
        # change place 

        pass
    def ends_expedition(self):
        #TODO implements a method that handles the end of the expedition
        #can you finish the game-> yes/no 
        #show statistics

        pass    
        
   
