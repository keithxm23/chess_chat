import sqlite3

con = sqlite3.connect('moves.db')
cur = con.cursor()

cur.execute('''CREATE TABLE videos (date text, yt_id text)''')

con.commit()

con.close()
