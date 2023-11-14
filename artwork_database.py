import sqlite3 as sql
import pandas as pd
import matplotlib.pyplot as plt

'''
Good practice as Class
Good practice one opening?
Good practice one Commit???
test!!!
'''

class Database(object):
    
    DB_LOCATION = "testing_database"

    def __init__(self):
        self.conn = sql.connect(Database.DB_LOCATION)
        self.c = self.conn.cursor()
        
    def fetchall(self):
        return self.c.fetchall()

    def fetchone(self):
        return self.c.fetchone()

    def execute(self, new_data):
        self.c.execute(new_data)

    def create_table_players(self):
        players = '''
            CREATE TABLE IF NOT EXISTS Players 
                        ([pid] INTEGER not NULL PRIMARY KEY,
                        [name] STRING UNIQUE,
                        [score] INTEGER)
            '''
        self.execute(players)
        
    def create_table_images(self):
        images = '''
            CREATE TABLE IF NOT EXISTS Images
                        ([iid] INTEGER not NULL PRIMARY KEY, 
                        [name] STRING,
                        [artist] STRING,
                        [room] STRING,
                        [type] STRING)
            '''
        self.execute(images)
        
    def create_table_guess(self):
        guess = '''
            CREATE TABLE IF NOT EXISTS Guess
                        ([pid] INTEGER,
                        [iid] INTEGER, 
                        [guess] STRING,                        
                        FOREIGN Key (iid) REFERENCES Images ON DELETE CASCADE, 
                        FOREIGN KEy (pid) REFERENCES Players ON DELETE CASCADE)
            '''
        self.execute(guess)
        
    def create_db(self):
        self.create_table_players()
        self.create_table_images()
        self.create_table_guess()

    def init_images(self, name: str, artist: str, room: str, type: str):
        initImage = f'''
                    INSERT INTO Images (name, artist, room, type) VALUES
                    ('{name}','{artist}','{room}','{type}')
                    '''  
        self.execute(initImage)
        
    def give_images(self):
        images = '''
            SELECT iid, room, type
            FROM Images
            '''
        self.execute(images)
        return self.fetchall()
   
    def begin_game_name(self, name):
        try:
            InsertName = '''
            INSERT Into Players (name) VALUES
                ('{}')
            '''.format(name)
            
            self.execute(InsertName)
        except sql.IntegrityError:
            print('This name is already in use')
        except:
            print('There is an issue')    

    def retrieve_pid(self, player):
        pid_search = '''SELECT pid FROM Players WHERE name = '{}' '''.format(player)
        self.execute(pid_search)
        pid = self.fetchone()
        return pid[0]
    
    def update_DB(self, player, guesses):
        #room argument only needed to check integrity...if already done in db -> nor needed
        try: 
            pid = self.retrieve_pid(player)
        except TypeError:
            print("This name does not exist. Please check again")
        except: 
            print("There is an issue")
        

        #insert can be done multiple times -> would this be an issue? No, only one try
        #someway to use update
        for (iid,guess) in guesses:
            GuessesUpdate =  f'''
            INSERT INTO Guess (pid, iid, guess) values({pid},{iid},'{guess}')
            '''
            self.execute(GuessesUpdate)
        
        #commit?
        #self.commit()
    
    '''
    Define getScore and update score
    '''
    def getScore(self, player):
        try: 
            pid = self.retrieve_pid(player)
        except TypeError:
            print("This name does not exist. Please check again")
        except: 
            print("There is an issue")
    
        Count = f'''
        SELECT Count(*)
        FROM Guess
        JOIN Images
        ON Guess.iid = Images.iid
        WHERE pid = '{pid}' and type = guess
        '''
        
        self.execute(Count)
        score = self.fetchone()
        return score[0]
    
    def updateScore(self, player: str):
    
        try: 
            pid = self.retrieve_pid(player)
        except TypeError:
            print("This name does not exist. Please check again")
        except: 
            print("There is an issue")
            
        count = self.getScore(player)
        
        score = f'''UPDATE Players
        SET score = '{count}'
        WHERE pid = '{pid}'
        '''
        self.execute(score)
    
    def score_numPlayer_total(self):
        #maybe close connection
        dict = {}
        count_images = '''Select count(*) from images'''
        self.execute(count_images)
        
        max_score = self.fetchone()[0]
        scores_range =  range(0, max_score+1)

        for score in scores_range:
            count_players = f'''SELECT count(name) 
                FROM Players
                WHERE score = {score}'''
                
            self.execute(count_players)
            
            num_players = self.fetchone()[0]
            dict[score] = num_players
            
        
        data_score = list(dict.keys())
        data_amount = list(dict.values())   
        plt.bar(data_score, data_amount)   
        plt.xlabel('Score')
        plt.ylabel('Number of Players')
        plt.title('Number of Players for Each Score')
        plt.show()
    
    def score_numPlayer_room(self, room: str):
        #maybe close connection first
        dict = {}
        count_per_room = F'''Select count(*) 
            FROM images
            WHERE room = {room}
            '''
        self.execute(count_per_room)
        
        max_score = self.fetchone()[0]
        scores_range =  range(0, max_score + 1)
        
        for score in scores_range:
            distinct_playername = f'''SELECT count(DISTINCT(p.name)) 
                FROM Players p, Images i
                WHERE p.score = {score} and i.room = {room}'''
                
            self.execute(distinct_playername)
            num_players = self.fetchone()[0]
            dict[score] = num_players
        
        data_score = list(dict.keys())
        data_amount = list(dict.values())   
        plt.bar(data_score, data_amount)   
        plt.xlabel('Score')
        plt.ylabel('Number of Players')
        plt.title(f'Room {room}')
        plt.show()
    
    
    def pie_chart():
        labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
        sizes = [15, 30, 45, 10]

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels)
        return None 
    
    def __enter__(self):
        return self

    def __exit__(self): 
        self.c.close()
        self.conn.close()
    
    def commit(self):
        self.conn.commit()

FakeDataUpdate = [('Peter', '1', [(1,'Real'),(2,'Real'),(3,'Real'),(4,'AI'),(5,'AI'),(6,'AI'),(7,'Real'),(8,'Real')])]

FakeDataImages = [('The laugh', 'Vincent', '1', 'AI'), 
                ('Happy', 'Vincent', '1', 'AI'), 
                ('The Thought', 'Vincent', '1', 'AI'),
                ('Sad', 'Vincent', '1', 'AI'),
                ('The', 'Josh', '1', 'Real'),
                ('What', 'Josh', '1', 'Real'),
                ('Two', 'Josh', '1', 'Real'),
                ('Mina Liso', 'Leonardo', '1', 'Real'),
                ('Sit', 'Michela', '2', 'Real'),
                ('Stand', 'Michela', '2', 'Real'),
                ('Walk', 'Michela', '2', 'Real'),
                ('Talk', 'DALLI', '2', 'AI'),
                ('Speak', 'DALLI', '2', 'AI'),
                ('Scream', 'DALLI', '2', 'AI')] 


db = Database()
db.create_db()

'''for (name, artist, room, type) in FakeDataImages:
    db.init_images(name,artist,room,type)
db.commit() '''   

for (name, room, guess) in FakeDataUpdate:
    db.update_DB(name, guess)
print(db.getScore('Peter'))
db.updateScore('Peter')
db.execute('''Select * from Players''')

print(db.fetchall())
db.score_numPlayer_room('1')


