import sqlite3
import pytz
import numpy as np # For array management
from datetime import datetime, timedelta
#import datetime # To generate timestamp

 ## Written by Kebene


class Session:
    def __init__(self, user_db):
        self.db = user_db
        self.con = sqlite3.connect(self.db, timeout=10)

    def make_time_table(self):

 
        # Loop through the range of train route IDs from 1 to 3
        for i in range(1, 4):
            #Define the SQL query to create the timetable table for the given train route ID
            query = f"""CREATE TABLE IF NOT EXISTS TIMETABLE_{i} AS
                            SELECT rs.stationID, tr.trainRouteID, rs.stationName, ss.departureTime AS Tid, toc.occurrenceDate
                            FROM StartStation ss
                            JOIN TrainOccurrence toc ON toc.startStationId=ss.startStationId
                            JOIN  TrainRoutes tr ON tr.startStationId = ss.startStationId
                            JOIN RailwayStations rs ON ss.stationID = rs.stationID
                            WHERE tr.trainRouteID = {i}
                            UNION
                            SELECT rs.stationID, tr.trainRouteID, rs.stationName, ts.departureTime AS Tid, toc.occurrenceDate
                            FROM TrainRoutes tr
                            JOIN TrainStops ts ON tr.trainRouteID = ts.trainRouteId
                            JOIN TrainOccurrence toc ON toc.trainRouteID = tr.trainRouteID 
                            JOIN RailwayStations rs ON ts.stationID = rs.stationID
                            WHERE tr.trainRouteID = {i}
                            UNION
                            SELECT rs.stationID, tr.trainRouteID, rs.stationName, es.arrivalTime AS Tid, toc.occurrenceDate
                            FROM EndStation es
                            JOIN TrainOccurrence toc ON toc.endStationId = es.endStationId
                            JOIN TrainRoutes tr ON tr.endStationId = es.endStationId
                            JOIN RailwayStations rs ON es.stationID = rs.stationID
                            WHERE tr.trainRouteID = {i}
                            ORDER BY occurrenceDate , Tid ASC;"""

            #Execute the SQL query to create the timetable table
            self.con.execute(query)
            
          

            query = "ALTER TABLE TIMETABLE_{} ADD DateTime datetime;".format(i)
            self.con.execute(query)
            self.con.commit()

            update_query = "UPDATE TIMETABLE_{} SET DateTime = strftime('%Y-%m-%d %H:%M', occurrenceDate || ' ' || Tid);".format(i)
            self.con.execute(update_query)
            self.con.commit()

        
def main():

    user_session = Session('railwaydatabase.db')
    user_session.make_time_table()

if __name__ == '__main__':
    main()
            