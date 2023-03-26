import sqlite3
import pytz
import numpy as np # For array management
from datetime import datetime, timedelta
#import datetime # To generate timestamp
from getpass import getpass
import re 
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
            print("4. Enter necessary data for purchasing tickets for Nordlandsbanen routes.")
            print("5. Find and purchase available tickets for a desired train route.")
            print("6. View information about purchases for future trips.")
            print("0. Exit.")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.find_routes_for_station_on_weekday()
            elif choice == "2":
                self.search_train_routes_between_stations()
            elif choice == "3":
                self.register_customer()
            elif choice == "4":
                self.enter_purchase_data()
            elif choice == "5":
                self.find_and_purchase_tickets()
            elif choice == "6":
                self.view_purchase_history()
            elif choice == "0":
                break
            else:
                print("Invalid choice.")

    def find_routes_for_station_on_weekday(self):
        station_name = input("Enter the name of the station: ")
        weekday = input("Enter the weekday from (MTWTF): ")
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
            print(row)

    def search_train_routes_between_stations(self):

        start_station = input("Enter the name of the starting station: ")
        end_station = input("Enter the name of the ending station: ")
        departure_datetime= input("Enter the date and time (YYYY-MM-DD HH:MM): ")






        departure_datetime = datetime.strptime(departure_datetime, "%Y-%m-%d %H:%M")
        # departure_time = input("Enter the time( HH:MM): ")
        # query = f"SELECT * FROM route_stops WHERE stop_name = '{start_station}'"
        departure_datetime_next = [departure_datetime, departure_datetime + timedelta(days=1, hours=9)]
        # Loop through the range of train route IDs from 1 to 3
        for i in range(2, 4):
            # #Define the SQL query to create the timetable table for the given train route ID
            # query = f"""CREATE TABLE TIMETABLE_{i} AS
            #                 SELECT rs.stationID, tr.trainRouteID, rs.stationName, ss.departureTime AS Tid, toc.occurrenceDate
            #                 FROM StartStation ss
            #                 JOIN TrainOccurrence toc ON toc.startStationId=ss.startStationId
            #                 JOIN  TrainRoutes tr ON tr.startStationId = ss.startStationId
            #                 JOIN RailwayStations rs ON ss.stationID = rs.stationID
            #                 WHERE tr.trainRouteID = {i}
            #                 UNION
            #                 SELECT rs.stationID, tr.trainRouteID, rs.stationName, ts.departureTime AS Tid, toc.occurrenceDate
            #                 FROM TrainRoutes tr
            #                 JOIN TrainStops ts ON tr.trainRouteID = ts.trainRouteId
            #                 JOIN TrainOccurrence toc ON toc.trainRouteID = tr.trainRouteID 
            #                 JOIN RailwayStations rs ON ts.stationID = rs.stationID
            #                 WHERE tr.trainRouteID = {i}
            #                 UNION
            #                 SELECT rs.stationID, tr.trainRouteID, rs.stationName, es.arrivalTime AS Tid, toc.occurrenceDate
            #                 FROM EndStation es
            #                 JOIN TrainOccurrence toc ON toc.endStationId = es.endStationId
            #                 JOIN TrainRoutes tr ON tr.endStationId = es.endStationId
            #                 JOIN RailwayStations rs ON es.stationID = rs.stationID
            #                 WHERE tr.trainRouteID = {i}
            #                 ORDER BY occurrenceDate , Tid ASC;"""

            # #Execute the SQL query to create the timetable table
            # self.con.execute(query)
            
          

            # query = "ALTER TABLE TIMETABLE_{} ADD DateTime datetime;".format(i)
            # self.con.execute(query)
            # self.con.commit()

            # update_query = "UPDATE TIMETABLE_{} SET DateTime = strftime('%Y-%m-%d %H:%M:%S', occurrenceDate || ' ' || Tid);".format(i)
            # self.con.execute(update_query)
            # self.con.commit()

            #next_data = data + timedelta(day=1)  # add 1 minute to the datetime object to get the next data
            # Define the SQL query to select the station names, departure time, and occurrence date for the given train route ID
            
  
            
            for departure_datetime in departure_datetime_next:

    
                query = f"""
            SELECT occurrenceDate,Tid
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
                #result.append (self.con.execute(query))
                for row in result:
                    if row is not None:
                        print(f"Train Route ID {i}:")   
                        print(row)
                    else:
                        print("No results found.")


                
            


            #Execute the SQL query to select the station names, departure time, and occurrence date
            #result = self.con.execute(query)

            # Print the results
            # Print the results if there are any
            # for row in result:
            #     if row is not None:
            #         print(f"Train Route ID {i}:")   
            #         print(row)
            #     else:
            #         print("No results found.")
            

    def register_customer(self):
        customerName = input("Enter your name: ")
        #email = input("Enter your email address: ")
        # Prompt user to enter a valid email address
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

    def enter_purchase_data(self):
        print("Enter the following information to purchase tickets for Nordlandsbanen routes.")
        customer_id = input("Enter your customer ID: ")
        route_id = input("Enter the route ID: ")
        departure_date = input("Enter the departure date (YYYY-MM-DD): ")
        num_tickets = input("Enter the number of tickets: ")
        query = f"INSERT INTO purchases (customer_id, route_id, departure_date, num_tickets) VALUES ({customer_id}, {route_id}, '{departure_date}', {num_tickets})"
        self.db.execute(query)
        print("Purchase data entered successfully.")

    def find_and_purchase_tickets(self):
        # name= input("Enter your name: ")
        # email = ""
        # while not check_email(email):
        #     email = input("Enter email address: ")
        #     if not check_email(email):
        #         print("Invalid email address. Please try again.")
        # #query=f"SELECT ID FROM Customers WHERE ID = {email} "
        # result = self.con.execute("SELECT COUNT(*) FROM Customers WHERE email=?",(email,))

        # for row in result:
        #     if not row[0]:
        #         print("Email address not found in database, Register first!")
        #         return 0
        
        # # Close the database connection
        
        # result_id = []
        start_station = input("Enter the name of the starting station: ")
        
        end_station = input("Enter the name of the ending station: ")
        departure_datetime = input("Enter the departure date (YYYY-MM-DD HH:MM): ")

        # for i in range(2, 4):
        #     query = f"""
        #         SELECT trainRouteID,occurrenceDate,Tid
        #         FROM TIMETABLE_{i} 
        #         WHERE DateTime BETWEEN (
        #             SELECT DateTime
        #             FROM TIMETABLE_{i} 
        #             WHERE stationName = '{start_station}'  
        #             AND DateTime >='{departure_datetime}' 
        #         ) AND (
        #             SELECT DateTime
        #             FROM TIMETABLE_{i} 
        #             WHERE stationName = '{end_station}'
        #             AND DateTime >='{departure_datetime}' 
        #         ) AND stationName = '{start_station}'"""
        
        # # calling the fuction to get id
        
        #     result = self.con.execute(query)

        #     routes = []
        #     for row in result:
        #     #route_id = row

        #         print("just testing if this could work" , row)
        #     query= f""" SELECT occurenceID FROM OCCURENCE_TABLE where 
        #     """
        customerID=1
        occurrenceID=3

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

        
        query=f"SELECT orderID FROM CustomerOrders WHERE customerID='{customerID}'AND occurrenceID='{occurrenceID}'AND orderDate='{orderDate}'"
        result=self.con.execute(query)
        for row in result:
            orderID=row
        
        added = False
        for ticket in range(1, int(numChairTickets) + 1):
            for i in range(1, 13):
                seatID = i
                query = "INSERT INTO ChairTickets (occurrenceID, orderID, seatID, startStationId, endStationId) VALUES (?, ?, ?, ?, ?)"
                values=(occurrenceID, orderID, seatID, startStationId, endStationId)
                self.con.execute(query, values)
                if self.con.total_changes > 0:
                    # If a seat ID has been added, set added to True and break out of the loop
                    added = True
                    break
            if added:
                # If a seat ID has been added, return the seat ID and break out of the outer loop
                return seatID
        if not added:
            # If the loop has finished without adding a seat ID, raise an exception or handle the error
            raise Exception("No available seat IDs")





        added = False
        for ticket in range(1, int(numBedTickets) + 1):
            for i in range(1, 13):
                bedID = i
                query = f"INSERT INTO BedTickets (occurrenceID, orderID, bedID, startStationId, endStationId) VALUES (?, ?, ?, ?, ?)"
                values=(occurrenceID, orderID, seatID, startStationId, endStationId)
                self.con.execute(query, values)
                if self.con.total_changes > 0:
                    # If a bed ID has been added, set added to True and break out of the loop
                    added = True
                    break
            if added:
                # If a bed ID has been added, return the bed ID and break out of the outer loop
                return bedID
        if not added:
            # If the loop has finished without adding a bed ID, raise an exception or handle the error
            raise Exception("No available bed IDs")

            





            # query = f"SELECT * FROM route_stops WHERE route_id = {route_id} AND stop_name = '{end_station}'"
            # end_station_result = self.db.execute(query)
            # if end_station_result:
            #     query = f"SELECT * FROM purchases WHERE route_id = {route_id} AND departure_date = '{departure_date}'"
            #     purchase_result = self.db.execute(query)
            #     num_tickets_purchased = 0
            #     for purchase_row in purchase_result:
            #         num_tickets_purchased += purchase_row[4]
            #     if num_tickets_purchased < row[6]:
            #         routes.append((route_id, row[3]))
        if not routes:
            print("No available tickets for this route on this date.")
        else:
            routes = sorted(routes, key=lambda x: x[1])
            for route in routes:
                print(f"Route {route[0]} departs at {route[1]}")
            route_choice = input("Enter the ID of the route you would like to purchase tickets for: ")
            num_tickets = input("Enter the number of tickets you would like to purchase: ")
            customer_id = input("Enter your customer ID: ")
            query = f"INSERT INTO purchases (customer_id, route_id, departure_date, num_tickets) VALUES ({customer_id}, {route_choice}, '{departure_date}', {num_tickets})"
            self.db.execute(query)
            print("Tickets purchased successfully.")

    def view_purchase_history(self):
        customer_id = input("Enter your customer ID: ")
        query = f"SELECT purchases.departure_date, route_stops.route_id, route_stops.route_name, route_stops.departure_time, purchases.num_tickets FROM purchases JOIN route_stops ON purchases.route_id = route_stops.route_id WHERE purchases.customer_id = {customer_id} ORDER BY purchases.departure_date, route_stops.departure_time"
        result = self.db.execute(query)
        if result:
            print("Your purchase history:")
            for row in result:
                print(f"Date: {row[0]}, Route: {row[1]} {row[2]}, Departure Time: {row[3]}, Number of Tickets: {row[4]}")
        else:
            print("No purchase history found.")

def main():

    user_session = Session('tester.db')
    user_session.run()

if __name__ == '__main__':
    main()