import sqlite3 as sql
import pandas as pd
import matplotlib.pyplot as plt


def connectDB():
    conn = sql.connect('test_database') 
    c = conn.cursor()
    return c, conn


#before game
def createDB():
    c,conn = connectDB()

    c.execute('''
            CREATE TABLE IF NOT EXISTS Players 
                        ([pid] INTEGER not NULL PRIMARY KEY,
                        [name] STRING UNIQUE,
                        [score] INTEGER)
            ''')
            
    c.execute('''
            CREATE TABLE IF NOT EXISTS Images
                        ([iid] INTEGER not NULL PRIMARY KEY, 
                        [name] STRING,
                        [artist] STRING,
                        [room] STRING,
                        [type] STRING)
            ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS Guess
                        ([guess] CHAR,
                        [iid] INTEGER, 
                        [pid] INTEGER,
                        FOREIGN Key (iid) REFERENCES Images, 
                        FOREIGN KEy (pid) REFERENCES Players)
            ''')

    conn.commit()
    c.close()
    conn.close()


#before game
def InitializeImages(name: str, artist: str, room: str, type: str):
    #add a way to give image ids to code 
    c,conn = connectDB()
    initImage = f'''
    Insert into Images (name, artist, room, type) Values
    ('{name}','{artist}','{room}','{type}')
    '''  
    c.execute(initImage)
    conn.commit()
    c.close()
    conn.close()


#begin game
def insertStartofGame(name: str):
    #maybe issue need to update guess as well...add pid
    c,conn = connectDB()
    try:
        c.execute(
        '''
        INSERT Into Players (name) VALUES
            ('{}')
        '''.format(name))
        
        conn.commit()
    except sql.IntegrityError:
        print('This name is already in use')
    except:
        print('There is an issue')
        
    c.close()
    conn.close()
    
    
#after each room
def updateDBperRoom(player: str, guesses: list[tuple]): 
    #add integrity check
    #only commit if all images from the db
    #only if name in db
    c,conn = connectDB()
    pid = getPID(player)
    
    for (Image,guess) in guesses:
        GuessesUpdate =  f'''
        UPDATE Guess
        SET guess = '{guess}'
        WHERE pid = {pid} and iid = {Image}
        '''
        c.execute(GuessesUpdate)
    conn.commit()
    c.close()
    conn.close()


#help function
def getPID(player: str):
    c, conn = connectDB()
    c.execute(
    '''SELECT pid FROM Players WHERE name = '{}' '''.format(player))
    pid = c.fetchone()
    c.close()
    conn.close()
    return pid[0]
    
    
#help function
def getScore(player: str):
    #only if player exists
    c, conn = connectDB()
    
    pid = getPID(player)
    Count = f'''
    SELECT Count(*)
    FROM Guess
    INNER JOIN Images
    ON Guess.iid = Images.iid
    WHERE pid = '{pid}' and type = guess
    '''
    
    c.execute(Count)
    counter = c.fetchone()
    score = counter[0]
    c.close()
    conn.close()
    return score


#when player exits game    
def updateScore(player: str):
    #only if player exists
    pid = getPID(player)
    count = getScore(player)
    
    c, conn = connectDB()
    score = f'''UPDATE Players
    SET score = '{count}'
    WHERE pid = '{pid}'
    '''
    c.execute(score)
    
    conn.commit()
    c.close()
    conn.close()


#after game
def viewHscore():
    c,conn = connectDB()
    c.execute('''
              
    CREATE VIEW IF NOT EXISTS Highscore
    AS SELECT p.name, p.score
    FROM Players p 
    ORDER BY p.score DESC
    LIMIT 3;
              
    ''')

    conn.commit()
    conn.close()


#statistic 1
def score_numPlayer_total():
    c, conn = connectDB()

    dict = {}

    c.execute(
        '''Select count(*) from images'''
    )
    max_score = c.fetchone()[0]+1
    scores_range =  range(0, max_score)

    for score in scores_range:
        c.execute(
            f'''SELECT count(name) 
            FROM Players
            WHERE score = {score}'''
        )
        num_players = c.fetchone()[0]
        dict[score] = num_players
        
    c.close
    conn.close
    
    data_score = list(dict.keys())
    data_amount = list(dict.values())   
    plt.bar(data_score, data_amount)   
    plt.xlabel('Score')
    plt.ylabel('Number of Players')
    plt.title('Number of Players for Each Score')
    plt.show()


#statistic 2 (not sure if works for all rooms)
def score_numPlayer_room(room: str):
    c, conn = connectDB()
    
    dict = {}
    
    c.execute(
        F'''Select count(*) 
        FROM images
        WHERE room = {room}
        '''
    )
    
    max_score = c.fetchone()[0]+1
    scores_range =  range(0, max_score)
    
    for score in scores_range:
        c.execute(
            f'''SELECT count(DISTINCT(p.name)) 
            FROM Players p, Images i
            WHERE p.score = {score} and i.room = {room}'''
        )
        num_players = c.fetchone()[0]
        dict[score] = num_players
    c.close
    conn.close
    
    data_score = list(dict.keys())
    data_amount = list(dict.values())   
    plt.bar(data_score, data_amount)   
    plt.xlabel('Score')
    plt.ylabel('Number of Players')
    plt.title(f'Room {room}')
    plt.show()
    
    
    
    
# testing
guesses = [(1,'REAL'),(2,'REAL'),(3,'REAL'),(4,'AI'),(5,'AI'),(6,'AI')]
    

c, conn = connectDB()
c.execute('''
        SELECT * FROM images
        ''')
print(c.fetchall())
#add statistic
