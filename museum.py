import numpy as np
pieces_number = 15
class artwork:
    categories = {}
    def __init__(name,category,artist):
        self.name = name
        self.category = category
        self.artist = artist
        if self.category in categories:
            categories[self.category][self.name] = self.artist
        else:
            categories[self.category] = {self.name: (self.artist)}
            
    def iscorrectguess(category,name,artist):
        try:
            correct_guess = artork.categories[category][name]
        except:
            print("you are trying to access a non existing entry in the guess")
        if correct_guess == "AI" and artist == "AI":
            return True
        elif correct_guess != "AI" and artist != "AI":
            return True
        else:
            return False
        
        
class player:
    def __init__(name):
        self.name = name
        self.place = ""
    def guess(self, artname, isrealpainter):
        #TODO implements a guess method that updates some sort of tracker
        pass
    def change_place(self, new_place):
        #TODO implements a method that updated the place and saves the progress
        pass
    def ends_expedition(self):
        #TODO implements a method that handles the end of the expedition
        pass    


