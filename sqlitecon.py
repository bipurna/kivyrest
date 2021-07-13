import sqlite3
import os , sys
from sqlite3 import Error

conn = None

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS contacts
               (id INTEGER PRIMARY KEY, name text NOT NULL, address text NOT NULL, email text NOT NULL, phone text NOT NULL)''')
        
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
def display(db_file,id=None):
    rows_list = []
    if id == None:
        try:
            conn = sqlite3.connect(db_file)
            c = conn.cursor()
            c.execute("SELECT * FROM contacts")
            rows = c.fetchall()
            for row in rows:
                rows_list.append(row)
                
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()
    else:
        try:
            conn = sqlite3.connect(db_file)
            c = conn.cursor()
            c.execute("SELECT * FROM contacts WHERE id=?",(id,))
            rows = c.fetchone()
            rows_list.append(rows)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()
    return rows_list

def insert_data_db(db_file,n,add,em,ph):
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        params = (n,add,em,ph)
        c.execute("INSERT INTO contacts(name, address, email, phone) VALUES (?,?,?,?)",params)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
            
def delete_entry(db_file,id):
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute("DELETE FROM contacts WHERE id = ?",(id,))
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
            
def update_data(db_file,id,name,address,email,phone):
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute("UPDATE contacts SET name = ?, address=?,email=?,phone=? WHERE id = ?",(name,address,email,phone,id))
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    
