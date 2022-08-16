print('Bismillah', '\n', 'testing')
import sqlite3

conn = sqlite3.connect('CMS.db')
cur = conn.cursor()
from datetime import date


# a parent class will deal inputs to the table
class CashManagement:

    def __init__(self, category, subcategory, descrip, amt, inputdate):
        # initialize instances for class
        self.category = category
        self.subcategory = subcategory
        self.descrip = descrip
        self.amt = amt
        self.inputdate = inputdate

    # creating method to input data to category
    def inputData_category(self):
        with conn:
            cur.execute('''INSERT OR IGNORE INTO category (nameCat) VALUES (?)  ''', (self.category,))
            # INSERT OR IGNORE
            # cur.execute("INSERT or IGNORE INTO category VALUES (:id,:category) ", {'id': None, 'category': self.category})
            # cur.execute("INSERT INTO category VALUES (:id,:category) ", {'id': None, 'category': self.category})

    # method to fetch category id via its name to use this category id in description table and subcategory table
    def fetch_categoryid(self):
        with conn:
            cur.execute("SELECT id FROM category WHERE nameCat = ? ", (self.category,))
        return cur.fetchone()[0]

    # method to input category_id and subcategory name to the subcategory table
    def inputdata_subcategory(self, category_id):
        with conn:
            cur.execute('''INSERT OR IGNORE INTO subcategory (category_id, namesubCat) VALUES (? ,?)  ''',
                        (category_id, self.subcategory))

    # method to fetch subcategory id to save the id to description table
    def fetch_subcategoryid(self):
        with conn:
            cur.execute("SELECT id FROM subcategory WHERE namesubCat = ? ", (self.subcategory,))
            return cur.fetchone()[0]

    # input category id and subcategory id to description table
    def inputdata_description(self, category_id, subcategory_id):
        with conn:
            cur.execute(
                '''INSERT OR IGNORE INTO description (category_id,subcategory_id, description, amount,inputdate) VALUES (?,? ,?, ?,?)  ''',
                (category_id, subcategory_id, self.descrip, self.amt, self.inputdate))

    # taking sum of amount in description table
    def addamount(self):
        with conn:
            cur.execute('''SELECT sum(amount) FROM description''')
            value = cur.fetchone()
            print('amount from function', value)
        return value

    # this method to call all the methods and input all the data to respective tables
    def inputcompletedata(self):
        CashManagement.inputData_category(self)
        category_id = CashManagement.fetch_categoryid(self)
        CashManagement.inputdata_subcategory(self, category_id)
        subcategory_id = CashManagement.fetch_subcategoryid(self)
        CashManagement.inputdata_description(self, category_id, subcategory_id)
        # FinalData = CashManagement.retrievecompletedata(self)
        # return FinalData

    # method to retrieve data from table
    def retrievecompletedata(self):
        # selecting variables to show main window, Connecting table with JOIN to fetch values
        with conn:
            cur.execute('''SELECT voucher_no, category.nameCat, subcategory.namesubCat, description.description ,description.amount,description.inputdate 
            FROM category JOIN subcategory JOIN description on category.id = subcategory.category_id and subcategory.id = description.subcategory_id''')
            data = cur.fetchall()
            print('data', data)
            # sum amount to get total amount
            cur.execute('''SELECT sum(description.amount) 
                            FROM category 
                            JOIN subcategory 
                            JOIN description 
                            on category.id = subcategory.category_id 
                            and subcategory.id = description.subcategory_id''')
            sumamount = cur.fetchall()
        return data, sumamount

    # method to retrieve data by any month
    def retrievecompletedatabymonth(self, startdate, enddate):
        # BETWEEN is creating a range of dates of user input
        with conn:
            cur.execute('''SELECT description.voucher_no,category.nameCat, subcategory.namesubCat, description.description, description.amount, description.inputdate
                       FROM category JOIN subcategory JOIN description ON category.id = subcategory.category_id and subcategory.id = description.subcategory_id
                         WHERE (inputdate BETWEEN :startdate AND :enddate)''',
                        {'startdate': startdate, 'enddate': enddate})
            data = cur.fetchall()
            # fetching total amount
            cur.execute('''SELECT sum(description.amount) FROM category JOIN subcategory JOIN description ON category.id = subcategory.category_id and subcategory.id = description.subcategory_id
                         WHERE (inputdate BETWEEN :startdate AND :enddate) ''',
                        {'startdate': startdate, 'enddate': enddate})
            amount = cur.fetchall()
            return data, amount


# **********************************************************CHILD CLASSS TO RETRIEVE BY category********************************************************************************
# this class was separate to make the code more modular and easier to understand

class Fetchbycategory(CashManagement):
    def __init__(self, category, subcategory, startdate, enddate):
        # initialize instances for child class
        self.category = category
        self.subcategory = subcategory
        self.startdate = startdate
        self.enddate = enddate

    # method to retrieve data by category
    def retrievebycategory(self):
        # fetch category and subcategory id of user inputs
        catid = CashManagement.fetch_categoryid(self)
        subcatid = CashManagement.fetch_subcategoryid(self)
        print("-----",catid,subcatid)
        # print(self.category, self.subcategory, self.startdate, self.enddate)
        # Query to connect tables on the basis category id and subcategory id and date
        with conn:
            cur.execute('''SELECT description.voucher_no,category.nameCat, subcategory.namesubCat, description.description, description.amount, description.inputdate
                FROM category JOIN subcategory JOIN description ON category.id = subcategory.category_id
                  WHERE category.id = :catid and subcategory.id = :subcatid
                    and description.category_id = :catid and description.subcategory_id = :subcatid and (inputdate BETWEEN :startdate AND :enddate)''',
                        {'catid': catid, 'subcatid': subcatid, 'startdate': self.startdate, 'enddate': self.enddate})
            data = cur.fetchall()
            # Query to fetching total amount
            cur.execute('''SELECT sum(description.amount)
                       FROM category JOIN subcategory JOIN description ON category.id = subcategory.category_id  
                         WHERE category.id = :catid and subcategory.id = :subcatid 
                           and description.category_id = :catid and description.subcategory_id = :subcatid and (inputdate BETWEEN :startdate AND :enddate)''',
                        {'catid': catid, 'subcatid': subcatid, 'startdate': self.startdate, 'enddate': self.enddate})
            sumamount = cur.fetchall()
            return sumamount, data

    # to take cash which is added to account
    def inputcashflowdata(self, CashIN, date):
        print("input cash", CashIN, 'date', date)
        #  Query to inset user input cash to the db
        with conn:
            cur.execute(''' INSERT into cashflow (CashIN,DOI) VALUES(?,?)''', (CashIN, date))

    # to fetch out cash from database
    def retrievecashflowdata(self):
        # query tos sum cash in the db and fetch out
        with conn:
            cur.execute('''SELECT sum(CashIN) from cashflow''')
        return cur.fetchall()

    # fetch input cash from particular dates
    def retrievecashflowdatacl(self, strtdate, endate):
        with conn:
            cur.execute('''SELECT CashIN,DOI from cashflow WHERE (DOI BETWEEN :startdate AND :enddate) ''',
                        {'startdate': strtdate, 'enddate': endate})
        return cur.fetchall()

