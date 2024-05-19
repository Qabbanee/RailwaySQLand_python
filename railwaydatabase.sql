BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "RailwayStations" (
	"stationID"	INTEGER NOT NULL,
	"stationName"	VARCHAR(100),
	"altitude"	FLOAT,
	PRIMARY KEY("stationID")
);
CREATE TABLE IF NOT EXISTS "TrackSection" (
	"sectionID"	INTEGER NOT NULL,
	"sectionName"	VARCHAR(100) NOT NULL,
	"drivingEnergy"	VARCHAR(100) NOT NULL,
	"startStationID"	INT NOT NULL,
	"endStationID"	INT NOT NULL,
	PRIMARY KEY("sectionID"),
	FOREIGN KEY("startStationID") REFERENCES "RailwayStations"("stationID") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("endStationID") REFERENCES "RailwayStations"("stationID") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "SubSections" (
	"subSectionID"	INTEGER NOT NULL,
	"trackSectionID"	INTEGER NOT NULL,
	"subSectionLength_km"	FLOAT,
	"trackType"	VARCHAR(10),
	"startStationId"	INTEGER NOT NULL,
	"endStationID"	INTEGER NOT NULL,
	PRIMARY KEY("subSectionID","trackSectionID"),
	FOREIGN KEY("endStationID") REFERENCES "RailwayStations"("stationID") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("trackSectionID") REFERENCES "TrackSection"("sectionID") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("startStationId") REFERENCES "RailwayStations"("stationID") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Operator" (
	"operatorID"	INTEGER NOT NULL,
	"operatorName"	VARCHAR(100),
	PRIMARY KEY("operatorID")
);
CREATE TABLE IF NOT EXISTS "CarType" (
	"carTypeID"	INTEGER NOT NULL,
	"operatorID"	INTEGER NOT NULL,
	"typeName"	VARCHAR(100),
	PRIMARY KEY("carTypeID","operatorID"),
	FOREIGN KEY("operatorID") REFERENCES "Operator"("operatorID") on update cascade on delete cascade
);
CREATE TABLE IF NOT EXISTS "ChairCar" (
	"chairCarID"	INTEGER NOT NULL,
	"CarTypeID"	INTEGER NOT NULL,
	"operatorID"	INTEGER NOT NULL,
	"numberOfSeatRows"	INTEGER,
	"numberOfSeatsPerRow"	INTEGER,
	PRIMARY KEY("chairCarID","operatorID"),
	FOREIGN KEY("CarTypeID","operatorID") REFERENCES "CarType"("carTypeID","operatorID") on update cascade on delete cascade
);
CREATE TABLE IF NOT EXISTS "SleepingCar" (
	"sleepingCarID"	INTEGER NOT NULL,
	"carTypeID"	INTEGER NOT NULL,
	"operatorID"	INTEGER NOT NULL,
	"numberOfCompartments"	INTEGER,
	PRIMARY KEY("sleepingCarID","operatorID"),
	FOREIGN KEY("carTypeID","operatorID") REFERENCES "CarType"("carTypeID","operatorID") on update cascade on delete cascade
);
CREATE TABLE IF NOT EXISTS "SleepingCompartment" (
	"compartmentID"	INTEGER NOT NULL,
	"sleepingCarID"	INTEGER NOT NULL,
	"compartmentNumber"	INTEGER,
	"numberOfBeds"	INTEGER,
	"operatorID"	INTEGER NOT NULL,
	PRIMARY KEY("compartmentID"),
	FOREIGN KEY("sleepingCarID","operatorID") REFERENCES "SleepingCar"("sleepingCarID","operatorID") on update cascade on delete cascade
);
CREATE TABLE IF NOT EXISTS "Bed" (
	"bedID"	INTEGER NOT NULL,
	"compartmentID"	INTEGER NOT NULL,
	"bedNumber"	INTEGER NOT NULL,
	"bedType"	VARCHAR(10),
	PRIMARY KEY("bedID"),
	FOREIGN KEY("compartmentID") REFERENCES "SleepingCompartment"("compartmentID") on update cascade on delete cascade
);
CREATE TABLE IF NOT EXISTS "Seat" (
	"seatID"	INTEGER,
	"seatNr"	INTEGER NOT NULL,
	"rowNumber"	INTEGER NOT NULL,
	"chairCarID"	INTEGER NOT NULL,
	"operatorID"	INTEGER NOT NULL,
	PRIMARY KEY("seatID"),
	FOREIGN KEY("chairCarID","operatorID") REFERENCES "ChairCar"("chairCarID","operatorID") on update cascade on delete cascade
);
CREATE TABLE IF NOT EXISTS "CarArrangements" (
	"arrangementID"	INTEGER NOT NULL,
	"carNumber"	INTEGER NOT NULL,
	"carTypeID"	INTEGER NOT NULL,
	"operatorID"	INTEGER NOT NULL,
	PRIMARY KEY("arrangementID"),
	FOREIGN KEY("carTypeID","operatorID") REFERENCES "CarType"("carTypeID","operatorID") on update cascade on delete cascade
);
CREATE TABLE IF NOT EXISTS "StartStation" (
	"startStationId"	INTEGER NOT NULL,
	"departureTime"	TIME NOT NULL,
	"stationID"	INTEGER NOT NULL,
	PRIMARY KEY("startStationId"),
	FOREIGN KEY("stationID") REFERENCES "RailwayStations"("stationID") on update cascade on delete cascade
);
CREATE TABLE IF NOT EXISTS "EndStation" (
	"endStationId"	INTEGER NOT NULL,
	"arrivalTime"	TIME NOT NULL,
	"stationID"	INTEGER NOT NULL,
	PRIMARY KEY("endStationId"),
	FOREIGN KEY("stationID") REFERENCES "RailwayStations"("stationID") on update cascade on delete cascade
);
CREATE TABLE IF NOT EXISTS "TrainRoutes" (
	"trainRouteID"	INTEGER NOT NULL,
	"operatorID"	INTEGER NOT NULL,
	"startStationId"	INTEGER NOT NULL,
	"endStationId"	INTEGER NOT NULL,
	"direction"	VARCHAR(10) NOT NULL,
	"runningDays"	CHAR(7) NOT NULL,
	PRIMARY KEY("trainRouteID"),
	FOREIGN KEY("startStationId") REFERENCES "StartStation"("startStationId") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("endStationId") REFERENCES "EndStation"("endStationId") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("operatorID") REFERENCES "Operator"("operatorID") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "TrainStops" (
	"trainStopId"	INT NOT NULL,
	"trainRouteId"	INT NOT NULL,
	"arrivalTime"	TIME NOT NULL,
	"departureTime"	TIME NOT NULL,
	"stationID"	INTEGER NOT NULL,
	PRIMARY KEY("trainStopId"),
	FOREIGN KEY("stationID") REFERENCES "RailwayStations"("stationID") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("trainRouteID") REFERENCES "TrainRoutes"("trainRouteID") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "RouteCarArrangements" (
	"trainRouteID"	INTEGER NOT NULL,
	"arrangementID"	INTEGER NOT NULL,
	PRIMARY KEY("trainRouteID"),
	FOREIGN KEY("arrangementID") REFERENCES "CarArrangements"("arrangementID") on update cascade on delete cascade,
	FOREIGN KEY("trainRouteID") REFERENCES "TrainRoutes"("trainRouteID") on update cascade on delete cascade
);
CREATE TABLE IF NOT EXISTS "Customers" (
	"customerID"	INTEGER,
	"customerName"	VARCHAR(100),
	"email"	VARCHAR(100),
	"mobile"	VARCHAR(10),
	PRIMARY KEY("customerID")
);
CREATE TABLE IF NOT EXISTS "TrainOccurrence" (
	"occurrenceID"	INTEGER NOT NULL,
	"trainRouteID"	INTEGER,
	"occurrenceDate"	DATE NOT NULL,
	"startStationId"	INTEGER,
	"endStationId"	INTEGER,
	PRIMARY KEY("occurrenceID"),
	FOREIGN KEY("startStationId") REFERENCES "StartStation"("startStationId"),
	FOREIGN KEY("trainRouteID") REFERENCES "TrainRoutes"("trainRouteID") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("endStationId") REFERENCES "EndStation"("endStationId")
);
CREATE TABLE IF NOT EXISTS "TIMETABLE_1" (
	"stationID"	INT,
	"trainRouteID"	INT,
	"stationName"	TEXT,
	"Tid"	NUM,
	"occurrenceDate"	NUM,
	"DateTime"	datetime
);
CREATE TABLE IF NOT EXISTS "TIMETABLE_2" (
	"stationID"	INT,
	"trainRouteID"	INT,
	"stationName"	TEXT,
	"Tid"	NUM,
	"occurrenceDate"	NUM,
	"DateTime"	datetime
);
CREATE TABLE IF NOT EXISTS "TIMETABLE_3" (
	"stationID"	INT,
	"trainRouteID"	INT,
	"stationName"	TEXT,
	"Tid"	NUM,
	"occurrenceDate"	NUM,
	"DateTime"	datetime
);
CREATE TABLE IF NOT EXISTS "CustomerOrders" (
	"orderID"	INTEGER,
	"customerID"	INTEGER NOT NULL,
	"occurrenceID"	INTEGER,
	"orderDate"	DATE NOT NULL,
	"numChairTickets"	INTEGER,
	"numBedTickets"	INTEGER,
	PRIMARY KEY("orderID"),
	FOREIGN KEY("customerID") REFERENCES "Customers"("customerID") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Bedtickets" (
	"ticketID"	INTEGER,
	"orderID"	INTEGER NOT NULL,
	"occurrenceID"	INTEGER NOT NULL,
	"bedID"	INTEGER NOT NULL,
	"startStationId"	INTEGER NOT NULL,
	"endStationId"	INTEGER NOT NULL,
	CONSTRAINT "uniqueTicket" UNIQUE("occurrenceID","bedID"),
	PRIMARY KEY("ticketID"),
	FOREIGN KEY("bedID") REFERENCES "Bed"("bedID"),
	FOREIGN KEY("occurrenceID") REFERENCES "TrainOccurrence"("occurrenceID"),
	FOREIGN KEY("startStationId") REFERENCES "RailwayStations"("stationID"),
	FOREIGN KEY("orderID") REFERENCES "CustomerOrders"("orderID"),
	FOREIGN KEY("endStationId") REFERENCES "RailwayStations"("stationID")
);
CREATE TABLE IF NOT EXISTS "ChairTickets" (
	"ticketID"	INTEGER,
	"occurrenceID"	INTEGER NOT NULL,
	"orderID"	INTEGER NOT NULL,
	"seatID"	INTEGER NOT NULL,
	"startStationId"	INTEGER NOT NULL,
	"endStationId"	INTEGER NOT NULL,
	CONSTRAINT "uniqueTicket" UNIQUE("occurrenceID","seatID","startStationId","endStationId"),
	PRIMARY KEY("ticketID"),
	FOREIGN KEY("seatID") REFERENCES "Seat"("seatID"),
	FOREIGN KEY("startStationId") REFERENCES "RailwayStations"("stationID"),
	FOREIGN KEY("orderID") REFERENCES "CustomerOrders"("orderID"),
	FOREIGN KEY("occurrenceID") REFERENCES "TrainOccurrence"("occurrenceID"),
	FOREIGN KEY("endStationId") REFERENCES "RailwayStations"("stationID")
);
INSERT INTO "RailwayStations" VALUES (1,'Trondheim',5.1);
INSERT INTO "RailwayStations" VALUES (2,'Steinkjer',3.6);
INSERT INTO "RailwayStations" VALUES (3,'Mosjøen',6.8);
INSERT INTO "RailwayStations" VALUES (4,'Mo i Rana',3.5);
INSERT INTO "RailwayStations" VALUES (5,'Fauske',34.0);
INSERT INTO "RailwayStations" VALUES (6,'Bodø',4.1);
INSERT INTO "TrackSection" VALUES (1,'Nordland','Diesel',1,6);
INSERT INTO "SubSections" VALUES (1,1,120.0,'double',1,2);
INSERT INTO "SubSections" VALUES (2,1,280.0,'single',2,3);
INSERT INTO "SubSections" VALUES (3,1,90.0,'single',3,4);
INSERT INTO "SubSections" VALUES (4,1,170.0,'single',4,5);
INSERT INTO "SubSections" VALUES (5,1,60.0,'single',5,6);
INSERT INTO "Operator" VALUES (1,'SJ');
INSERT INTO "CarType" VALUES (1,1,'Chair Car');
INSERT INTO "CarType" VALUES (2,1,'Sleeping Car');
INSERT INTO "ChairCar" VALUES (1,1,1,3,4);
INSERT INTO "SleepingCar" VALUES (1,2,1,4);
INSERT INTO "SleepingCompartment" VALUES (1,1,1,2,1);
INSERT INTO "SleepingCompartment" VALUES (2,1,2,2,1);
INSERT INTO "SleepingCompartment" VALUES (3,1,3,2,1);
INSERT INTO "SleepingCompartment" VALUES (4,1,4,2,1);
INSERT INTO "Bed" VALUES (1,1,1,'Lower');
INSERT INTO "Bed" VALUES (2,1,2,'Upper');
INSERT INTO "Bed" VALUES (3,2,1,'Lower');
INSERT INTO "Bed" VALUES (4,2,2,'Upper');
INSERT INTO "Bed" VALUES (5,3,1,'Lower');
INSERT INTO "Bed" VALUES (6,3,2,'Upper');
INSERT INTO "Bed" VALUES (7,4,1,'Lower');
INSERT INTO "Bed" VALUES (8,4,2,'Upper');
INSERT INTO "Seat" VALUES (1,1,1,1,1);
INSERT INTO "Seat" VALUES (2,2,1,1,1);
INSERT INTO "Seat" VALUES (3,3,1,1,1);
INSERT INTO "Seat" VALUES (4,4,1,1,1);
INSERT INTO "Seat" VALUES (5,5,2,1,1);
INSERT INTO "Seat" VALUES (6,6,2,1,1);
INSERT INTO "Seat" VALUES (7,7,2,1,1);
INSERT INTO "Seat" VALUES (8,8,2,1,1);
INSERT INTO "Seat" VALUES (9,9,3,1,1);
INSERT INTO "Seat" VALUES (10,10,3,1,1);
INSERT INTO "Seat" VALUES (11,11,3,1,1);
INSERT INTO "Seat" VALUES (12,12,3,1,1);
INSERT INTO "StartStation" VALUES (1,'07:49',1);
INSERT INTO "StartStation" VALUES (2,'23:05',1);
INSERT INTO "StartStation" VALUES (3,'08:11',4);
INSERT INTO "EndStation" VALUES (1,'17:34',6);
INSERT INTO "EndStation" VALUES (2,'09:05',6);
INSERT INTO "EndStation" VALUES (3,'14:13',1);
INSERT INTO "TrainRoutes" VALUES (1,1,1,1,'Main','MTWtF');
INSERT INTO "TrainRoutes" VALUES (2,1,2,2,'Main','MTWtF');
INSERT INTO "TrainRoutes" VALUES (3,1,3,3,'Opposite','MTWtF');
INSERT INTO "TrainStops" VALUES (1,1,'09:40','09:51',2);
INSERT INTO "TrainStops" VALUES (2,1,'13:10','13:20',3);
INSERT INTO "TrainStops" VALUES (3,1,'14:20','14:31',4);
INSERT INTO "TrainStops" VALUES (4,1,'16:35','16:49',5);
INSERT INTO "TrainStops" VALUES (5,2,'00:45','00:57',2);
INSERT INTO "TrainStops" VALUES (6,2,'04:30','04:41',3);
INSERT INTO "TrainStops" VALUES (7,2,'05:45','05:55',4);
INSERT INTO "TrainStops" VALUES (8,2,'08:10','08:19',5);
INSERT INTO "TrainStops" VALUES (9,3,'09:05','09:14',3);
INSERT INTO "TrainStops" VALUES (10,3,'12:20','12:31',2);
INSERT INTO "Customers" VALUES (1,'Maria','maria@gmail.com','89299999');
INSERT INTO "Customers" VALUES (2,'Ahmed','ami@yahoo.com','90121222');
INSERT INTO "TrainOccurrence" VALUES (1,1,'2023-04-03',1,1);
INSERT INTO "TrainOccurrence" VALUES (2,1,'2023-04-04',1,1);
INSERT INTO "TrainOccurrence" VALUES (3,NULL,'2023-04-03',2,NULL);
INSERT INTO "TrainOccurrence" VALUES (4,NULL,'2023-04-04',2,NULL);
INSERT INTO "TrainOccurrence" VALUES (5,3,'2023-04-03',3,3);
INSERT INTO "TrainOccurrence" VALUES (6,3,'2023-04-04',3,3);
INSERT INTO "TrainOccurrence" VALUES (7,2,'2023-04-04',NULL,2);
INSERT INTO "TrainOccurrence" VALUES (8,2,'2023-04-05',NULL,2);
INSERT INTO "TIMETABLE_1" VALUES (1,1,'Trondheim','07:49','2023-04-03','2023-04-03 07:49');
INSERT INTO "TIMETABLE_1" VALUES (2,1,'Steinkjer','09:51','2023-04-03','2023-04-03 09:51');
INSERT INTO "TIMETABLE_1" VALUES (3,1,'Mosjøen','13:20','2023-04-03','2023-04-03 13:20');
INSERT INTO "TIMETABLE_1" VALUES (4,1,'Mo i Rana','14:31','2023-04-03','2023-04-03 14:31');
INSERT INTO "TIMETABLE_1" VALUES (5,1,'Fauske','16:49','2023-04-03','2023-04-03 16:49');
INSERT INTO "TIMETABLE_1" VALUES (6,1,'Bodø','17:34','2023-04-03','2023-04-03 17:34');
INSERT INTO "TIMETABLE_1" VALUES (1,1,'Trondheim','07:49','2023-04-04','2023-04-04 07:49');
INSERT INTO "TIMETABLE_1" VALUES (2,1,'Steinkjer','09:51','2023-04-04','2023-04-04 09:51');
INSERT INTO "TIMETABLE_1" VALUES (3,1,'Mosjøen','13:20','2023-04-04','2023-04-04 13:20');
INSERT INTO "TIMETABLE_1" VALUES (4,1,'Mo i Rana','14:31','2023-04-04','2023-04-04 14:31');
INSERT INTO "TIMETABLE_1" VALUES (5,1,'Fauske','16:49','2023-04-04','2023-04-04 16:49');
INSERT INTO "TIMETABLE_1" VALUES (6,1,'Bodø','17:34','2023-04-04','2023-04-04 17:34');
INSERT INTO "TIMETABLE_2" VALUES (1,2,'Trondheim','23:05','2023-04-03','2023-04-03 23:05');
INSERT INTO "TIMETABLE_2" VALUES (2,2,'Steinkjer','00:57','2023-04-04','2023-04-04 00:57');
INSERT INTO "TIMETABLE_2" VALUES (3,2,'Mosjøen','04:41','2023-04-04','2023-04-04 04:41');
INSERT INTO "TIMETABLE_2" VALUES (4,2,'Mo i Rana','05:55','2023-04-04','2023-04-04 05:55');
INSERT INTO "TIMETABLE_2" VALUES (5,2,'Fauske','08:19','2023-04-04','2023-04-04 08:19');
INSERT INTO "TIMETABLE_2" VALUES (6,2,'Bodø','09:05','2023-04-04','2023-04-04 09:05');
INSERT INTO "TIMETABLE_2" VALUES (1,2,'Trondheim','23:05','2023-04-04','2023-04-04 23:05');
INSERT INTO "TIMETABLE_2" VALUES (2,2,'Steinkjer','00:57','2023-04-05','2023-04-05 00:57');
INSERT INTO "TIMETABLE_2" VALUES (3,2,'Mosjøen','04:41','2023-04-05','2023-04-05 04:41');
INSERT INTO "TIMETABLE_2" VALUES (4,2,'Mo i Rana','05:55','2023-04-05','2023-04-05 05:55');
INSERT INTO "TIMETABLE_2" VALUES (5,2,'Fauske','08:19','2023-04-05','2023-04-05 08:19');
INSERT INTO "TIMETABLE_2" VALUES (6,2,'Bodø','09:05','2023-04-05','2023-04-05 09:05');
INSERT INTO "TIMETABLE_3" VALUES (4,3,'Mo i Rana','08:11','2023-04-04','2023-04-04 08:11');
INSERT INTO "TIMETABLE_3" VALUES (3,3,'Mosjøen','09:14','2023-04-04','2023-04-04 09:14');
INSERT INTO "TIMETABLE_3" VALUES (2,3,'Steinkjer','12:31','2023-04-04','2023-04-04 12:31');
INSERT INTO "TIMETABLE_3" VALUES (1,3,'Trondheim','14:13','2023-04-04','2023-04-04 14:13');
INSERT INTO "TIMETABLE_3" VALUES (4,3,'Mo i Rana','08:11','2023-04-05','2023-04-05 08:11');
INSERT INTO "TIMETABLE_3" VALUES (3,3,'Mosjøen','09:14','2023-04-05','2023-04-05 09:14');
INSERT INTO "TIMETABLE_3" VALUES (2,3,'Steinkjer','12:31','2023-04-05','2023-04-05 12:31');
INSERT INTO "TIMETABLE_3" VALUES (1,3,'Trondheim','14:13','2023-04-05','2023-04-05 14:13');
COMMIT;
