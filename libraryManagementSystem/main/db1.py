import sqlite3

conn = sqlite3.connect("library.db")
c = conn.cursor()

c.execute("create table Books (Id primarykey auto increment,Title varchar(50),Genre varchar(50),Author varchar(50),year integer,Availablity boolean)")

conn.commit()
conn.close()