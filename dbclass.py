import sqlite3
con = sqlite3.connect('CMS.db')
cur = con.cursor()

# *******************************TO DROP TABLE PLZ UNCOMMENT***********************************************
# cur.execute(''' DROP TABLE catagory''')
# cur.execute(''' DROP TABLE subcatagory''')
# cur.execute(''' DROP TABLE description''')
# cur.execute('''DROP TABLE cashflow''')

cur.execute('''CREATE TABLE catagory
        ( id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        nameCat VARCHAR UNIQUE)''')
cur.execute('''CREATE TABLE subcatagory
        (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        catagory_id VARCHAR,
        namesubCat VARCHAR UNIQUE)''')

cur.execute('''CREATE TABLE description 
        (voucher_no INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        catagory_id INTEGER ,
        subcatagory_id VARCHAR,
        description VARCHAR, amount INTEGER, inputdate TEXT )''')
cur.execute('''CREATE TABLE cashflow 
        (OB INTEGER ,
        DOI TEXT )''')

# Save (commit) the changes
con.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()