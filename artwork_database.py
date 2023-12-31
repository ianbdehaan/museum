import sqlite3 as sql
import matplotlib.pyplot as plt
import os

class Database(object):
    
    DB_LOCATION = "database"

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

    def init_images(self, name: str, room: str, type: str):
        initImage = f'''
                    INSERT INTO Images (name, room, type) VALUES
                    ('{name}','{room}','{type}')
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
        #maybe use return statements    


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

    
    def getScore(self, player):
        try: 
            pid = self.retrieve_pid(player)
        except TypeError:
            print("This name does not exist. Please check again")
        except: 
            print("There is an issue")

        Count = f'''SELECT Count(*)
                    FROM Guess
                    WHERE pid = '{pid}' and guess = 'True' '''
        
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
        plt.close()
    
    
    # score_numPlayer_room
    def score_numPlayer_room(self, room: str):
        dict = {}
        count_per_room = F'''Select count(*) 
            FROM images
            WHERE room = '{room}'
            '''
        self.execute(count_per_room)
        max_score = self.fetchone()
        
        scores_range =  range(0, max_score + 1)
        
        for score in scores_range:
            distinct_playername = f'''SELECT count(*) 
                FROM Players p, Images i
                WHERE p.score = {score} and i.room = '{room}' '''
                
            self.execute(distinct_playername)
            num_players = self.fetchone()
            print(num_players)
            dict[score] = num_players
            print(dict[score])
            
        data_score = list(dict.keys())
        data_amount = list(dict.values())   
        plt.bar(data_score, data_amount)   
        plt.xlabel('Score')
        plt.ylabel('Number of Players')
        plt.title(f'Room {room}')
        plt.savefig(f'score_histogram_{room}.png')
        plt.close()
      
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
        plt.close()
    
    def __exit__(self): 
        self.c.close()
        self.conn.close()
    
    def commit(self):
        self.conn.commit()

if __name__ == "__main__":
    FakeDataUpdate = [
    ('peter', '1', [(1,'TRUE'),(2,'FALSE'),(3,'TRUE'),(4,'TRUE'),(5,'FALSE'),(6,'TRUE'),(7,'FALSE'),(8,'FALSE')])
    ]


    FakeDataImages = [('opart_ai_1',	'AI',	'OpArt'), ('opart_2', 'Human', 'OpArt'),
('Screenshot 2023-11-08 at 13_25_23','Human', 'OpArt'),
('Screenshot 2023-11-08 at 13_25_41' ,'Human','OpArt'),
('opartai5',	'AI',	'OpArt'),
('opartai6',	'AI',	'OpArt'),
('opart_3', 'Human',	'OpArt'),
('opart_ai_3',	'AI',	'OpArt'),
('opart_ai_2',	'AI',	'OpArt'),
('WhatsApp Image 2023-11-07 at 12_36_37 (1)','Human',	'Cubism'),
('WhatsApp Image 2023-10-11 at 10_16_18',	'AI',	'Cubism'),
('WhatsApp Image 2023-10-11 at 10_18_52',	'Human',	'Cubism'),
('WhatsApp Image 2023-11-07 at 12_36_37',	'AI',	'Cubism'),
('f521d3e5759c43229966b7714a828449_ComfyUI_144983_',	'Human',	'Cubism'),
('WhatsApp Image 2023-10-11 at 10_14_01',	'Human',	'Cubism'),
('1b880a9d00344029bb285e90fb40709a_ComfyUI_143648__001',	'Human',	'Cubism'),
('WhatsApp Image 2023-10-11 at 10_14_00',	'AI',	'Cubism'),
('1861_jpg',	'AI',	'Cubism'),
('sur_3',	'Human',	'Surrealism'),
('sur_1',	'Human',	'Surrealism'),
('WhatsApp Image 2023-11-08 at 10_18_07',	'Human',	'Surrealism'),
('sur_2',	'Human',	'Surrealism'),
('ai_sur_4',	'AI',	'Surrealism'),
('ai_sur_3',	'AI',	'Surrealism'),
('ai_sur_1',	'AI',	'Surrealism'),
('sur_4',	'Human',	'Surrealism'),
('popart_1',	'Human',	'PopArt'),
('popart_2',	'Human',	'PopArt'),
('popart_3',	'Human',	'PopArt'),
('popart_4',	'Human',	'PopArt'),
('popart_5',	'Human',	'PopArt'),
 ('popart_ai_1',	'AI',	'PopArt'),
('popart_ai_2',	'AI',	'PopArt'),
('popart_ai_3',	'AI',	'PopArt'),
('popart_ai_4',	'AI',	'PopArt'),
('1',	'Human',	'Minimalism'),
('2', 'Human',	'Minimalism'),
('min_ai_7',	'AI',	'Minimalism'),
('min_ai_1',	'AI',	'Minimalism'),
('min_ai_4',	'AI',	'Minimalism'),
('3_001',	'Human',	'Minimalism'),
('4',	'Human',	'Minimalism')]
    
    db = Database()
    '''db.create_db()
    for (name, room, type) in FakeDataImages:
        db.init_images(name, room, type)
    db.commit()'''

    print(db.give_images())
    db.__exit__()
    
    








