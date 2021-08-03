import sqlite3
from datetime import datetime



def insert_yt_id(yt_id):
    try:
        con = sqlite3.connect('moves.db')
        cur = con.cursor()

        cur.execute(f"INSERT INTO videos VALUES ('{str(datetime.now())}','{yt_id}')")

        con.commit()
        con.close()
        return True
    except:
        return False


def check_id_present(yt_id):
    con = sqlite3.connect('moves.db')
    cur = con.cursor()

    cur.execute('SELECT * FROM videos WHERE yt_id=?', [yt_id])
    res = cur.fetchone()
    con.commit()
    con.close()

    print(res)
    if res:
        return True
    else:
        return False

def truncate():
    con = sqlite3.connect('moves.db')
    cur = con.cursor()

    cur.execute(f"DELETE FROM videos")

    con.commit()
    con.close()

def truncate_val(val):
    con = sqlite3.connect('moves.db')
    cur = con.cursor()

    cur.execute(f"DELETE FROM videos where yt_id=?", [val])

    con.commit()
    con.close()
#TODO Add method to run a query and display result
