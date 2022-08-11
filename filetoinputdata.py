print('Bismillah','\n', 'test')
import sqlite3
conn = sqlite3.connect('CMS.db')
cur = conn.cursor()
from datetime import date

class CashManagement:

    def __init__(self,catagory, subcatagory, descrip,amt,inputdate):
        self.catagory = catagory
        self.subcatagory = subcatagory
        self.descrip = descrip
        self.amt = amt
        self.inputdate = inputdate




    def inputData_catagory(self):
        with conn:
            cur.execute('''INSERT OR IGNORE INTO catagory (nameCat) VALUES (?)  ''',(self.catagory,))
            # INSERT OR IGNORE
            # cur.execute("INSERT or IGNORE INTO catagory VALUES (:id,:catagory) ", {'id': None, 'catagory': self.catagory})
             # cur.execute("INSERT INTO catagory VALUES (:id,:catagory) ", {'id': None, 'catagory': self.catagory})



    def fatch_catagoryid(self):
        with conn:
            cur.execute("SELECT id FROM catagory WHERE nameCat = ? ", (self.catagory, ))
            # IdCatagoryCatagory =
        return cur.fetchone()[0]





    def inputdata_subcatagory(self,catagory_id):
        with conn:
            cur.execute('''INSERT OR IGNORE INTO subcatagory (catagory_id, namesubCat) VALUES (? ,?)  ''',(catagory_id,self.subcatagory))




    def fatch_subcatagoryid(self):
        with conn:
            cur.execute("SELECT id FROM subcatagory WHERE namesubCat = ? ", (self.subcatagory,))
            # IdCatagoryCatagory =
            return cur.fetchone()[0]




    def inputdata_description(self,catagory_id,subcatagory_id):
        with conn:
            cur.execute('''INSERT OR IGNORE INTO description (catagory_id,subcatagory_id, description, amount,inputdate) VALUES (?,? ,?, ?,?)  ''',
                        (catagory_id,subcatagory_id, self.descrip, self.amt,self.inputdate))



    def addamount(self):
        with conn:
            cur.execute('''SELECT sum(amount) FROM description''')
            value = cur.fetchone()
            print('amount from function',value)
        return value



    def inputcompletedata(self):
        CashManagement.inputData_catagory(self)
        catagory_id = CashManagement.fatch_catagoryid(self)
        CashManagement.inputdata_subcatagory(self,catagory_id)
        subcatagory_id = CashManagement.fatch_subcatagoryid(self)
        CashManagement.inputdata_description(self,catagory_id,subcatagory_id)
        # FinalData = CashManagement.retrievecompletedata(self)
        # return FinalData


    def retrievecompletedata(self):
        catid = CashManagement.fatch_catagoryid(self)
        subcatid = CashManagement.fatch_subcatagoryid(self)
        with conn:
            # cur.execute('''SELECT catagory.nameCat,   subcatagory.namesubCat
            # FROM catagory JOIN subcatagory on catagory.id = :CAT and subcatagory.catagory_id = :subCat''', {'CAT': 4, 'subCat': 6})
            cur.execute('''SELECT voucher_no, catagory.nameCat,   subcatagory.namesubCat, description.description ,description.amount,description.inputdate 
            FROM catagory JOIN subcatagory JOIN description on catagory.id = subcatagory.catagory_id and subcatagory.id = description.subcatagory_id''')
            data = cur.fetchall()
            print('data',data)
            cur.execute('''SELECT sum(description.amount) 
                            FROM catagory 
                            JOIN subcatagory 
                            JOIN description 
                            on catagory.id = subcatagory.catagory_id 
                            and subcatagory.id = description.subcatagory_id''')
                        #      WHERE catagory.id = :catid and subcatagory.id = :subcatid 
                        #        and description.catagory_id = :catid and description.subcatagory_id = :subcatid ''',
                        # {'catid': catid, 'subcatid': subcatid})
            sumamount = cur.fetchall()
        return data,sumamount
    def retrievecompletedatabymonth(self,startdate,enddate):
        with conn:
            cur.execute('''SELECT description.voucher_no,catagory.nameCat, subcatagory.namesubCat, description.description, description.amount, description.inputdate
                       FROM catagory JOIN subcatagory JOIN description ON catagory.id = subcatagory.catagory_id and subcatagory.id = description.subcatagory_id
                         WHERE (inputdate BETWEEN :startdate AND :enddate)''',
                        {'startdate': startdate, 'enddate': enddate})
            data = cur.fetchall()
            cur.execute('''SELECT sum(description.amount) FROM catagory JOIN subcatagory JOIN description ON catagory.id = subcatagory.catagory_id and subcatagory.id = description.subcatagory_id
                         WHERE (inputdate BETWEEN :startdate AND :enddate) ''',
                        {'startdate': startdate, 'enddate': enddate})
            amount = cur.fetchall()
            return data,amount
# **********************************************************CHILD CLASSS TO RETRIEVE BY CATAGORY********************************************************************************


class Fetchbycatagory(CashManagement):
    def __init__(self,catagory,subcatagory,startdate,enddate):
        self.catagory = catagory
        self.subcatagory = subcatagory
        self.startdate = startdate
        self.enddate = enddate


    def retrievebycatagory(self):
        catid = CashManagement.fatch_catagoryid(self)
        subcatid = CashManagement.fatch_subcatagoryid(self)
        print(self.catagory,self.subcatagory,self.startdate,self.enddate)
        with conn:
            cur.execute('''SELECT description.voucher_no,catagory.nameCat, subcatagory.namesubCat, description.description, description.amount, description.inputdate
                FROM catagory JOIN subcatagory JOIN description ON catagory.id = subcatagory.catagory_id
                  WHERE catagory.id = :catid and subcatagory.id = :subcatid
                    and description.catagory_id = :catid and description.subcatagory_id = :subcatid and (inputdate BETWEEN :startdate AND :enddate)''',
                        {'catid': catid, 'subcatid': subcatid, 'startdate': self.startdate,'enddate':self.enddate})
            data = cur.fetchall()
            cur.execute('''SELECT sum(description.amount)
                       FROM catagory JOIN subcatagory JOIN description ON catagory.id = subcatagory.catagory_id  
                         WHERE catagory.id = :catid and subcatagory.id = :subcatid 
                           and description.catagory_id = :catid and description.subcatagory_id = :subcatid and (inputdate BETWEEN :startdate AND :enddate)''',
                    {'catid': catid, 'subcatid': subcatid, 'startdate': self.startdate, 'enddate': self.enddate})
            sumamount = cur.fetchall()
            return sumamount, data
    # def catagorydatacall(self):
    #     catagory_id = CashManagement.fatch_catagoryid(self)
    #     subcatagory_id = CashManagement.fatch_subcatagoryid(self)
    #     print("retrived records to print")
    #     value = CashManagement.fetchtoextrct(self)
    #     return value
    def inputcashflowdata(self,OB,date):
        print(OB,'date',date)
        with conn:
            cur.execute(''' INSERT into cashflow (OB,DOI) VALUES(?,?)''',(OB,date))

    def retrievecashflowdata(self):
        with conn:
            cur.execute('''SELECT sum(OB) from cashflow''')
        return cur.fetchall()
    def retrievecashflowdatacl(self,strtdate,endate):
        with conn:
            cur.execute('''SELECT OB,DOI from cashflow WHERE (DOI BETWEEN :startdate AND :enddate) ''',{'startdate': strtdate, 'enddate': endate})
        return cur.fetchall()
# *************************************************************  objects     ***************************************************


# data1 = CashManagement('Maintainance','paint','quarter paint 2 bucket',20000,'2021-10-16')
# data2 = CashManagement('Food','Lunch','Salan roti',900,'2021-10-16')
# data3 = CashManagement('Project','Zaman pvt ltd','Smokes',20000,'2021-11-16')
# data4 = CashManagement('Project','Rajby','Cables',9000,'2021-10-15')
# data5 = CashManagement('Project','Emaar','Inin Compact 2 loop',40000, '2021-09-17')
# data6 = CashManagement('Project', 'Avt', 'Smart loop', 60000, '2021-05-12')
# data7 = CashManagement('Project','Emaar','Cables 2mm',80000, '2021-06-12')
# data8 = CashManagement('Project','Emaar','smoke',55000,'2021-07-16')
# data9 = CashManagement('Project','Emaar','heat detectors',70000,'2021-10-09')
# data10 = CashManagement('Lunch','Aljibra house','sounder with flasher',60000,'2021-09-12')
# data11 = CashManagement('Project','Emaar','sounder with flasher',60000,'2021-09-12')
# list_data[circle], list_data[circle+1], list_data[circle+2],list_data[circle+3],list_data[circle+4
# colldata = [data1,data2,data3,data4,data5,data6,data7,data8,data9,data10,data11]
# # ********************************callclassfunctions*******************************
# for data in colldata:
#     CashManagement.inputcompletedata(data)
# dumydata = CashManagement('test', 'test', 'test', 0, '2021-10-27')




# %%%%%%%%%%%%%%%%%%%%%%%% MOnthly %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# month = date.today().month
# year= date.today().year
# monthstart = "{yy}-{mm}-{dd}".format(yy=year, mm = month, dd = '1')
# monthend = "{yy}-{mm}-{dd}".format(yy=year, mm = month, dd = '31')
# print(monthend,monthstart)

# %%%%%%%%%%%%%%%%%%%%%%%%%% all data %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# d,a = CashManagement.retrievecompletedatabymonth(None,monthstart,monthend)
# print('dataaa',d,'amountt',a)
# da,am = CashManagement.retrievecompletedata(dumydata)
# print('datacom',da,'compleamount',am)


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# print('input complete data',CashManagement.inputcompletedata(dumydata))
# data = Fetchbycatagory('Lunch','Aljibra house','2021-09-12','2021-09-20')
# print(CashManagement.retrievecompletedata(dumydata))
# print('catagory',Fetchbycatagory.retrievebycatagory(data))
#
# amt,data = CashManagement.retrievecompletedata(data11)
# Fetchbycatagory.inputcashflowdata(None,'30','3213')
# print(data)
# print(amnt[0][0])
# data = Fetchbycatagory('Project', 'Emaar','2021-05-12','2021-11-16')
# data = Fetchbycatagory('test', 'test','2021-10-27','2021-10-28')
# sumamt, catagorywisedata = Fetchbycatagory.retrievebycatagory(data)
# print('all', CashManagement.retrievecompletedata(data11))
# print(catagorywisedata)
# for data in catagorywisedata:
#     print(data)
# amount = list(Fetchbycatagory.addamount(data))
# print('total amount: ',amount)