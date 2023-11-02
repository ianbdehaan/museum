import numpy as np 
pieces_number = 15
class artwork:
    categories = {}
    def __init__(self, name,category,artist):
        categories = {}
        self.name = name
        self.category = category
        self.artist = artist
        if self.category in categories:
            categories[self.category][self.name] = self.artist
        else:
            categories[self.category] = {self.name: (self.artist)}
            
    def isCorrectGuess(self, category,name,artist):
        try:
            correct_guess = artwork.categories[category][name]
        except:
            print("you are trying to access a non existing entry in the guess")
        if correct_guess == "AI" and artist == "AI":
            return True
        elif correct_guess != "AI" and artist != "AI":
            return True
        else:
            return False
        
        
class player:
    def __init__(self, name):
        self.name = name
        self.place = ""
    def guess(self, category, artname, isrealpainter):
        #TODO implements a guess method that updates some sort of tracker
        if category != self.place: 
            #in this case we change rooms
            closeDoors()
            pass
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
        
   
