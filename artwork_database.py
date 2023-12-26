import sqlite3 as sql
import pandas as pd
import matplotlib.pyplot as plt



class Database(object):
    
    DB_LOCATION = "testing_database"

    def __init__(self):
        self.conn = sql.connect(Database.DB_LOCATION)
        self.c = self.conn.cursor()
        
    def fetchall(self):
        return self.c.fetchall()

    def fetchone(self):
        return self.c.fetchone()[0]

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

    #room as string
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
        self.commit()

    def retrieve_pid(self, player):
        pid_search = '''SELECT pid FROM Players WHERE name = '{}' '''.format(player)
        self.execute(pid_search)
        pid = self.fetchone()
        return pid
    
    def update_DB(self, player, guesses):
        
        '''Insert guesses from given Data for specific players'''
        
        try: 
            pid = self.retrieve_pid(player)
        except TypeError:
            print("This name does not exist. Please check again")
        except: 
            print("There is an issue")
        
        for (iid,guess) in guesses:
            GuessesUpdate =  f'''
            INSERT INTO Guess (pid, iid, guess) values({pid},{iid},'{guess}')
            '''
            self.execute(GuessesUpdate)
        self.commit()
    
    def getScore(self, player):
        try: 
            pid = self.retrieve_pid(player)
        except TypeError:
            print("This name does not exist. Please check again")
        except: 
            print("There is an issue")

        Count = f'''SELECT Count(*)
                    FROM Guess
                    WHERE pid = '{pid}' and guess = 'TRUE' '''
        
        self.execute(Count)
        score = self.fetchone()
        return score
    
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
        self.commit()
    
    def score_numPlayer_total(self):
        dict = {}
        count_images = '''Select count(*) from images'''
        self.execute(count_images)
        
        max_score = self.fetchone()
        scores_range =  range(0, max_score+1)

        for score in scores_range:
            count_players = f'''SELECT count(name) 
                FROM Players
                WHERE score = {score}'''
                
            self.execute(count_players)
            
            num_players = self.fetchone()
            dict[score] = num_players
            
        
        data_score = list(dict.keys())
        data_amount = list(dict.values())   
        plt.bar(data_score, data_amount)   
        plt.xlabel('Score')
        plt.ylabel('Number of Players')
        plt.title('Number of Players for Each Score')
        plt.savefig('score_histogram_total.png')
    
    def score_numPlayer_room(self, room: str):
        # close connection first
        dict = {}
        count_per_room = F'''Select count(*) 
            FROM images
            WHERE room = {room}
            '''
        self.execute(count_per_room)
        
        max_score = self.fetchone()
        scores_range =  range(0, max_score + 1)
        
        for score in scores_range:
            distinct_playername = f'''SELECT count(DISTINCT(p.name)) 
                FROM Players p, Images i
                WHERE p.score = {score} and i.room = '{room}' '''
                
            self.execute(distinct_playername)
            num_players = self.fetchone()
            dict[score] = num_players
        
        data_score = list(dict.keys())
        data_amount = list(dict.values())   
        plt.bar(data_score, data_amount)   
        plt.xlabel('Score')
        plt.ylabel('Number of Players')
        plt.title(f'Room {room}')
        plt.savefig(f'score_histogram_{room}.png')
      
    def pie_chart(self, player):
        total_players = '''Select count(*) from Players'''
        self.execute(total_players)
        amt_players = self.fetchone()

        score_player = f'''SELECT score 
                FROM Players
                WHERE name = '{player}' '''
        self.execute(score_player)
        score = self.fetchone()

        count_players = f'''SELECT count(name) 
                FROM Players
                WHERE score >= {score}'''
                
        self.execute(count_players)  
        num_players_with_greater_score = self.fetchone()
        print(num_players_with_greater_score)
            
        labels = 'You are in the best: ','Rest'
        sizes = [num_players_with_greater_score, amt_players-num_players_with_greater_score]

        fig, ax = plt.subplots()
        explode = (0.1,0) 
        ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        startangle=90)
        ax.axis('equal')
        
        plt.tight_layout()
        plt.savefig('pie_chart.png')
    
    def double_plot():
        
        return False
    
        
        
    
    def __exit__(self): 
        self.c.close()
        self.conn.close()
    
    def commit(self):
        self.conn.commit()

if __name__ == "__main__":
    FakeDataUpdate = [
    ('peter', '1', [(1,'TRUE'),(2,'FALSE'),(3,'TRUE'),(4,'TRUE'),(5,'FALSE'),(6,'TRUE'),(7,'FALSE'),(8,'FALSE')])
    ]

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
    
    for (name, painter, room, ai) in FakeDataImages:
        db.init_images(name, painter, room, ai)
    

    db.execute('''select * from guess''')
    print(db.fetchall())
    print(db.getScore('peter'))
    








