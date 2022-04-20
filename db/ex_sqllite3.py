import sqlite3
con = sqlite3.connect('data.db')
cObj = con.cursor()


#1.create table 
cObj.execute("CREATE TABLE users(id integer primary key autoincrement , name text , location text)")
con.commit()

#2.insert data 
cObj.execute("insert into users(name,location) values(?,?)",("noraphat","Bangkok"))
con.commit()

cObj.close()
con.close()
