import sqlite3
import pandas as pd


def connectDB():
    conn = sqlite3.connect('test_database') 
    c = conn.cursor()
    return c, conn

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

def insertStartofGame(name):

    c,conn = connectDB()
    c.execute(
    '''
    INSERT Into Players (name) VALUES
        ('{}')
    '''.format(name))

    conn.commit()
    c.close()
    conn.close()

def InitializeImages(name, artist, room, type):
      
    c,conn = connectDB()
    initImage = f'''
    Insert into Images (name, artist, room, type) Values
    ('{name}','{artist}','{room}','{type}')
    '''  
    c.execute(initImage)
    conn.commit()
    c.close()
    conn.close()

def updateDBperRoom(player, room, guesses: list[tuple]): 

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


def getPID(player):
    c, conn = connectDB()
    c.execute(
    '''SELECT pid FROM Players WHERE name = '{}' '''.format(player))
    pid = c.fetchone()
    c.close()
    conn.close()
    return pid[0]
    
 
def getScore(player):
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
    
def updateScore(player):
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


guesses = [(1,'AI'),(2,'AI'),(3,'AI'),(4,'AI'),(5,'AI'),(6,'AI')]

viewHscore()
c, conn = connectDB()



c.execute(
    '''
    SELECT * from Highscore
''')
print(pd.DataFrame(c.fetchall()))
c.close()
conn.close()


