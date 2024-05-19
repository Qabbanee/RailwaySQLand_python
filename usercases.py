import sqlite3
import pytz
import numpy as np # For array management
from datetime import datetime, timedelta
#import datetime # To generate timestamp
from getpass import getpass
import re 

## Written by Kebene


def check_email(email):
    # Regular expression for validating email addresses
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email)

def check_phone(phone):
    # Regular expression for validating phone numbers
    pattern = r"^\d{8}$"
    return re.match(pattern, phone)
class Session:
    def __init__(self, user_db):
        self.db = user_db
        self.con = sqlite3.connect(self.db, timeout=10)

    def run(self):
        print("Welcome to the Train app!")
        while True:
            print("\nWhat would you like to do?")
            print("1. Find all train routes for a station on a weekday.")
            print("2. Search for train routes between two stations based on date and time.")
            print("3. Register as a customer.")
            print("4. Find and purchase available tickets for a desired train route.")
            print("5. View information about purchases for future trips.")
            print("0. Exit.")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.find_routes_for_station_on_weekday()
            elif choice == "2":
                self.search_train_routes_between_stations()
            elif choice == "3":
                self.register_customer()
            elif choice == "4":
                self.enter_order_data()
            elif choice == "5":
                self.view_purchase_history()
            elif choice == "0":
                break
            else:
                print("Invalid choice.")

    # Finding routes by takin in station user case c)
    def find_routes_for_station_on_weekday(self):
        station_name = input("Enter the name of the station\n(Trondheim, Mosjøen, Mo i Rana, Fauske, Bodø): ")
        valid_weekdays = ["M", "T", "W", "t", "F"]
        weekday = input("Enter the weekday (M, T, W, t, or F): ")
        while weekday not in valid_weekdays:
            print("Invalid input. Please enter a valid weekday.")
            weekday = input("Enter the weekday (M, T, W, t, or F): ")
        query = f"SELECT tr.trainRouteID, rs.stationName \
               FROM TrainRoutes tr \
               JOIN StartStation ss ON tr.startStationId = ss.startStationId \
               JOIN RailwayStations rs ON ss.stationID = rs.stationID \
               WHERE rs.stationName = '{station_name}' AND runningDays LIKE '%{weekday}%' \
               UNION \
               SELECT tr.trainRouteID, rs.stationName \
               FROM TrainRoutes tr \
               JOIN TrainStops ts ON tr.trainRouteID = ts.trainRouteId \
               JOIN RailwayStations rs ON ts.stationID = rs.stationID \
               WHERE rs.stationName = '{station_name}' AND runningDays LIKE '%{weekday}%' \
               UNION \
               SELECT tr.trainRouteID, rs.stationName \
               FROM TrainRoutes tr \
               JOIN EndStation es ON tr.endStationId = es.endStationId \
               JOIN RailwayStations rs ON es.stationID = rs.stationID \
               WHERE rs.stationName = '{station_name}' AND runningDays LIKE  '%{weekday}%'"
        result = self.con.execute(query)
        for row in result:
            if row is not None:
                print("Train route" ,row[0])
            else: 
                print("Couldn't find any routes")

    #Usercase d) finding routes between two given station and datetime. I iterate trough all avleble routes
    def search_train_routes_between_stations(self):

        startStation = input("Enter the name of the starting station\n(Trondheim, Mosjøen, Mo i Rana, Fauske, Bodø): ")
        endStation = input("Enter the name of the ending station\n(Trondheim, Mosjøen, Mo i Rana, Fauske, Bodø): ")
        departureDatetime= input("Enter the date and time (YYYY-MM-DD HH:MM)\nExample date for this case 2023-04-03 00:00: ")

        departureDatetime = datetime.strptime(departureDatetime, "%Y-%m-%d %H:%M")
        
        #making a list to iterate through the date given and next day
        departure_datetime_next = [departureDatetime, departureDatetime + timedelta(days=1)] 
        # Loop through the range of train route IDs from 1 to 3
        for i in range(1, 4):
            
            for departure_datetime in departure_datetime_next:

                query = f"""
            SELECT occurrenceDate,Tid
            FROM TIMETABLE_{i} 
            WHERE DateTime BETWEEN (
                SELECT DateTime
                FROM TIMETABLE_{i} 
                WHERE stationName = '{startStation}'  
                AND DateTime >='{departure_datetime}' 
            ) AND (
                SELECT DateTime
                FROM TIMETABLE_{i} 
                WHERE stationName = '{endStation}'
                AND DateTime >='{departure_datetime}' 
            ) AND stationName = '{startStation}'"""
                result = self.con.execute(query)
                #result.append (self.con.execute(query))
                for row in result:
                    if row is not None:
                        print(f"Train Route {i}:")   
                        print(row[0],"at",row[1], "from",startStation)
                    else:
                        print("No results found.")

            #usercase e) regestering new customer 
    def register_customer(self):
        customerName = input("Enter your name: ")
        
        # Prompt user to enter a valid email address and phone
        email = ""
        while not check_email(email):
            email = input("Enter email address: ")
            if not check_email(email):
                print("Invalid email address. Please try again.")
        mobile = ""
        while not check_phone(mobile):
            mobile = input("Enter your mobile: ")
            if not check_phone(mobile):
                print("Invalid phone number. Please try again.")
        query = "INSERT INTO Customers (customerName, email, mobile) VALUES (?, ?, ?)"
        values = (customerName, email, mobile)
        self.con.execute(query, values)
        self.con.commit()
        print("Registration successful.")

    #Usercase g) taking order and gettin tickets
    def enter_order_data(self):
        
        name= input("Enter your name: ")
        email = ""
        while not check_email(email):
            email = input("Enter email address: ")
            if not check_email(email):
                print("Invalid email address. Please try again.")
        
        result = self.con.execute("SELECT COUNT(*) FROM Customers WHERE email=?",(email,))

        for row in result:
            if not row[0]:
                print("Email address not found in database, Register first!")
                return 0
        
        
        
        # result_id = []
        start_station = input("Enter the name of the starting station: ")
        
        end_station = input("Enter the name of the ending station: ")
        departure_datetime = input("Enter the departure date (YYYY-MM-DD HH:MM): ")
        print("Please, chose when you want to go?")
        choice = {}
        counter = 0
        for i in range(1, 4):
            query = f"""
                SELECT trainRouteID,occurrenceDate,Tid
                FROM TIMETABLE_{i} 
                WHERE DateTime BETWEEN (
                    SELECT DateTime
                    FROM TIMETABLE_{i} 
                    WHERE stationName = '{start_station}'  
                    AND DateTime >='{departure_datetime}' 
                ) AND (
                    SELECT DateTime
                    FROM TIMETABLE_{i} 
                    WHERE stationName = '{end_station}'
                    AND DateTime >='{departure_datetime}' 
                ) AND stationName = '{start_station}'"""
        
            result = self.con.execute(query)

            #routes = []
            counter
            for row in enumerate(result):
                counter +=1
                choice[counter] = row
                print("opition " + str(counter), row[1][1:])

        index = input("Your option: ")
        trainRouteID,occurrenceDate,Tid =  choice[int(index)][1]
        query = f"""SELECT  toc.occurrenceID
        FROM StartStation ss
        JOIN TrainOccurrence toc ON toc.startStationId=ss.startStationId
        JOIN  TrainRoutes tr ON tr.startStationId = ss.startStationId
        JOIN RailwayStations rs ON ss.stationID = rs.stationID
        WHERE tr.trainRouteID = {trainRouteID} AND toc.occurrenceDate='{occurrenceDate}' 
        """
        result=self.con.execute(query)
        occurrenceID=0
        for row in result:
            occurrenceID=row[0]
        
            
        query = f""" SELECT customerID 
        FROM Customers WHERE email='{email}'
        """
        result=self.con.execute(query)
        customerID =0
        for row in result:
            customerID =row[0]
         
        
        # set the timezone to your local timezone
        tz = pytz.timezone('Europe/Oslo')

        # get the current date and time with the correct timezone
        current_datetime = datetime.now(tz)

        orderDate = current_datetime.strftime("%Y-%m-%d %H:%M")   
       

        numChairTickets = input("How many chair tickets? ")
        numBedTickets= input("How many bed tickets? ")
        query= "INSERT INTO CustomerOrders(customerID,occurrenceID,orderDate,numChairTickets,numBedTickets) VALUES (?, ?, ?,?,?)"
        values = (customerID, occurrenceID, orderDate,numChairTickets,numBedTickets)
        self.con.execute(query, values)
        self.con.commit()

        #getting orderID
        query=f"SELECT orderID FROM CustomerOrders WHERE customerID='{customerID}'AND occurrenceID='{occurrenceID}'AND orderDate='{orderDate}'"
        result=self.con.execute(query)
        orderId=0
        for row in result:
            orderID=row[0]

        query=f"SELECT stationID FROM RailwayStations WHERE stationName='{start_station}'"
        result=self.con.execute(query)
        startStationId=0
        for row in result:
            startStationId=row[0]

        query=f"SELECT stationID FROM RailwayStations WHERE stationName='{end_station}'"
        result=self.con.execute(query)
        endStationId=0
        for row in result:
            endStationId=row[0]
        
        
        #Seat ID
        added = False
        ticket = 0
        #total 13 seat in a train
        for i in range(1, 13):
            if ticket >= int(numChairTickets):
                break
            seatID = i
            try:
                query = "INSERT INTO ChairTickets (occurrenceID, orderID, seatID, startStationId, endStationId) VALUES (?, ?, ?, ?, ?)"
                values = (occurrenceID, orderID, seatID, startStationId, endStationId)
                self.con.execute(query, values)
                self.con.commit()
                added = True
            except sqlite3.IntegrityError:
                added = False
            if added:
                ticket += 1
                query=f"SELECT seatNr,chairCarID FROM Seat WHERE seatID={seatID} "
                result=self.con.execute(query)
                for row in result:
                    print("Your seat nr. is:",row[0],"in chaircar nr",row[1])
        if not added:
            # If the loop has finished without adding a seat ID, raise an exception or handle the error
            print("No available seat")
            

        added = False
        ticket = 0
        #8 bed in a train
        for i in range(1, 8):
            if ticket >= int(numBedTickets):
                break
            bedID = i
            try:
                query = "INSERT INTO ChairTickets (occurrenceID, orderID, seatID, startStationId, endStationId) VALUES (?, ?, ?, ?, ?)"
                values = (occurrenceID, orderID, bedID, startStationId, endStationId)
                self.con.execute(query, values)
                self.con.commit()
                added = True
            except sqlite3.IntegrityError:
                added = False
            if added:
                ticket += 1
                query=f"SELECT bedNumber,compartmentID,bedType FROM Bed WHERE bedID={bedID} "
                result=self.con.execute(query)
                for row in result:
                    bedNumber=row[0]
                    compartmentID=row[1]
                    bedType=row[2]

                query=f"SELECT compartmentNumber, sleepingCarID FROM SleepingCompartment WHERE compartmentID={compartmentID} "
                result=self.con.execute(query)
                for row in result:
                    compartmentNumber=row[0]
                    carNr=row[1] 
                    print("Your bed nr. is:", bedNumber, "in Sleepincar nr", carNr, "compartment \n", compartmentNumber, "and is Type", bedType)
        if not added:
            # If the loop has finished without adding a bed ID, raise an exception or handle the error
            #raise Exception("No available bed")
            print("No available bed")
                     
        
        
 # usercase h) viewing information about purchases made for future trips for a user. 
    def view_purchase_history(self):

        email = ""
        while not check_email(email):
            email = input("Enter email address: ")
            if not check_email(email):
                print("Invalid email address. Please try again.")
       

        query = f""" SELECT customerID 
        FROM Customers WHERE email='{email}'
        """
        result=self.con.execute(query)
        customerID =0
        for row in result:
            customerID =row[0]

        
         # set the timezone to your local timezone
        tz = pytz.timezone('Europe/Oslo')

        # get the current date and time with the correct timezone
        current_datetime = datetime.now(tz)

        current_datetime = current_datetime.strftime("%Y-%m-%d")   
        query = f"""SELECT startStationId AS ROUTE , orderDate,numChairTickets,numBedTickets, occurrenceDate
        FROM Customers
        NATURAL JOIN CustomerOrders 
        NATURAL JOIN TrainOccurrence
        WHERE customerID='{customerID}'AND occurrenceDate >='{current_datetime}'"""
        
        result = self.con.execute(query)

        
        if result:
            print("Your purchase history:")
            for row in result:
                print(f"Route: {row[0]}, orderDate: {row[1]} , Number of Chair Tickets: {row[2]},Number of Bed Tickets: {row[3]} Occurrence Date: {row[4]}")
        else:
            print("No purchase history found.")

def main():

    user_session = Session('railwaydatabase.db')
    user_session.run()

if __name__ == '__main__':
    main()