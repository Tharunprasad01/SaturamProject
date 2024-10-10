import sqlite3

con = sqlite3.connect("UserAuthenticationSystem.db")
c = con.cursor()

c.execute("create table users (userId primarykey auto increment,Name varchar(40),password varchar(50))")
con.commit()
con.close()