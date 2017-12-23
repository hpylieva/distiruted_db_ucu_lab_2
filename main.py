#!/usr/bin/python

import psycopg2
from psycopg2._psycopg import DatabaseError

hostname = 'localhost'
username = 'postgres'
password = 't27sj4ph81!'
db1 = 'flt_booking'
db2 = 'htl_booking'
db3 = 'account'
#FLIGHT_BOOKING_PRICE = 100
#HOTEL_BOOKING_PRICE = 200
TOTAL_BOOKING_PRICE = 150 #FLIGHT_BOOKING_PRICE+HOTEL_BOOKING_PRICE


class DatabaseConnection:
    def __init__(self):
        try:
            self.flight = psycopg2.connect(host=hostname, user=username, password=password, dbname=db1)
            self.hotel = psycopg2.connect(host=hostname, user=username, password=password, dbname=db2)
            self.account = psycopg2.connect(host=hostname, user=username, password=password, dbname=db3)
            self.curFlight = self.flight.cursor()
            self.curHotel = self.hotel.cursor()
            self.curAccount = self.account.cursor()

            #self.curFlight.execute("SELECT MAX(booking_id) FROM flight_booking;")
            self.idFlight = 7 #list(self.curFlight.fetchall()[0])[0]+1
           # self.curHotel.execute("SELECT MAX(booking_id) FROM hotel_booking;")
            self.idHotel = 5 #list(self.curHotel.fetchall()[0])[0]+1
        except:
            "Cannot connect ot database"

    def performBooking(self):

        # fetching a random person from the database

        #self.curAccount.execute("SELECT * FROM account where client_name = 'Elsa' limit 1")
        #data = self.curAccount.fetchall()
        #account_id , client_name, amount= [1,'Nick',100]
        account_id, client_name, amount = [2,'Elsa',200]

        # creating booking commands
        flt_booking_command = 'INSERT INTO flight_booking(booking_id, client_name, flight_number, "from", "to", date) VALUES ('\
                          + str(self.idFlight) + ", '" + client_name + "', 'KA 123', 'IEV', 'LRK', '2017-11-12');"
        htl_booking_command = 'INSERT INTO hotel_booking (booking_id, client_name, hotel_name, arrival, departure) VALUES ('\
                          + str(self.idHotel) + ", '" + client_name + "', 'Rismus',  '2017-11-12', '2017-11-13');"
        funds_debiting_command = "UPDATE account SET amount=" + str(amount - TOTAL_BOOKING_PRICE) + " WHERE account_id =" \
                                 + str(account_id) + ";"

        self.idFlight = self.idFlight + 1
        self.idHotel = self.idHotel + 1



        # organizing 2PC
        self.flight.tpc_begin(self.flight.xid(42, 'transaction ID', 'connection 1'))
        self.hotel.tpc_begin(self.hotel.xid(42, 'transaction ID', 'connection 2'))
        self.account.tpc_begin(self.account.xid(42, 'transaction ID', 'connection 3'))


        try:

            self.curFlight.execute(flt_booking_command)
            self.flight.tpc_prepare()

            self.curHotel.execute(htl_booking_command)
            self.hotel.tpc_prepare()

            self.curAccount.execute(funds_debiting_command)
            self.account.tpc_prepare()

        except DatabaseError as exception:
            print (exception)
            self.flight.tpc_rollback()
            self.hotel.tpc_rollback()
            self.account.tpc_rollback()
        else:

            self.flight.tpc_commit()
            self.hotel.tpc_commit()
            self.account.tpc_commit()


            print(flt_booking_command)
            print(htl_booking_command)
            print(funds_debiting_command)

        # self.flight.commit()
        # debiting funds

        # self.account.commit()


        def __del__(self):
            self.flight.close()
            self.account.close()
            self.hotel.close()
            self.curFlight.close()
            self.curHotel.close()
            self.curAccount.close()

#--------------------BEGIN------------------------
if __name__ == '__main__':
    databaseConnection  = DatabaseConnection()
    databaseConnection.performBooking()

