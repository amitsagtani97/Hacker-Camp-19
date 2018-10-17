import MySQLdb
import config

class UsersData():
    def __init__(self):
        self.totalUsers = 0
        self.cursor = ""

    def connectData(self):
        print("Connecting to database..........")
        try:
            self.db = MySQLdb.connect(
                host = "localhost",
                user = config.rootUser,
                password = config.pwd,
                database = "mydb")
            print("Database Connected sucessfully.\n")
        except:
            print("Error occured in connecting to database...")
            print("Please create a database first.")
        
    def addUser(self, user, series):
        self.cursor = self.db.cursor()
        if self.totalUsers == 0:
            self.cursor.execute("Create Table Users (EmailID varchar(255) primary key,\
                                FavouriteTvShows varchar(255))")
            self.cursor.execute("Show tables")
            for tb in self.cursor:
                print(tb)
        
        newUser = RowData(user, series)
        newUser.executeData(self.cursor)
        
        self.totalUsers += 1  #increment users
        self.db.commit()
    
    def showUsersData(self):
        self.cursor.execute(" SELECT * FROM USERS ")
        # fetch all of the rows from the query
        data = self.cursor.fetchall ()
        # print the rows
        for row in data:
            print(row[0],":",row[1])
    
    def clearData(self):
        self.cursor.execute('Drop table users')


class RowData():
    def __init__(self, user, series):
        self.u_email = user
        self.u_shows = series

    def executeData(self, mycursor):
        sqlForm = "Insert into Users (EmailID,FavouriteTvShows) values (%s,%s)"
        user = [self.u_email,self.u_shows]
        mycursor.execute(sqlForm,user)