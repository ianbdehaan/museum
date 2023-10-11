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
                        [name] STRING,
                        [guess] STRING,
                        [score] INTEGER)
            ''')
            
    c.execute('''
            CREATE TABLE IF NOT EXISTS Images
                        ([iid] INTEGER not NULL PRIMARY KEY, 
                        [name] STRING,
                        [artist] STRING,
                        [room] INTEGER,
                        [category] STRING)
            ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS Guess
                        ([result] CHAR,
                        [iid] INTEGER, 
                        [pid] INTEGER,
                        FOREIGN Key (iid) REFERENCES Images, 
                        FOREIGN KEy (pid) REFERENCES Players)
            ''')

    conn.commit()

def insertValues():

    c,conn = connectDB()
    c.execute(
    '''
    INSERT Into Players (pid, name, score) VALUES
        (111, 'Leon', 1),
        (222, 'Peter', 2),
        (121, 'Mati', 3)
    ''')

    conn.commit()

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

c, conn = connectDB()
c.execute(
    '''
    SELECT * from Highscore
'''
)
print(pd.DataFrame(c.fetchall(), columns=['name','score']))


