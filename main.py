#!/usr/bin/python

import psycopg2

hostname = 'localhost'
username = 'postgres'
password = 't27sj4ph81!'
db1 = 'flt_booking'
db2 = 'htl_booking'
db3 = 'account'
FLIGHT_BOOKING_PRICE = 100
HOTEL_BOOKING_PRICE = 200

idFlight = 1
idBooking = 1

class DatabaseConnection:
    def __init__(self):
        try:
            self.flight = psycopg2.connect(host=hostname, user=username, password=password, dbname=db1)
            self.hotel = psycopg2.connect(host=hostname, user=username, password=password, dbname=db2)
            self.account = psycopg2.connect(host=hostname, user=username, password=password, dbname=db3)
            self.curFlight = self.flight.cursor()
            self.curHotel = self.hotel.cursor()
            self.curAccount = self.account.cursor()
            self.curFlight.execute("SELECT MAX(booking_id) FROM flight_booking;")
            self.idFlight = list(self.curFlight.fetchall()[0])[0]+1
        except:
            "Cannot connect ot database"

    def bookFlight(self):

        # fetching a random person from the database
        self.curAccount.execute("SELECT * FROM account limit 1")
        data = self.curAccount.fetchall()
        account_id , client_name, amount= list(data[0])

        # creating a booking
        booking_command = 'INSERT INTO flight_booking(booking_id, client_name, flight_number, "from", "to", date) VALUES ('\
                          + str(self.idFlight) + ", '" + client_name + "', 'KA 123', 'IEV', 'LRK', '2017-11-12');"

        self.idFlight = self.idFlight + 1
        print(booking_command)
        self.curFlight.execute(booking_command)
        self.flight.commit()
        # debiting funds
        funds_debiting_command = "UPDATE account SET amount=" + str(amount - FLIGHT_BOOKING_PRICE) + " WHERE account_id =" \
                                 + str(account_id) + ";"
        self.curAccount.execute(funds_debiting_command)
        self.account.commit()
        print(funds_debiting_command)

        def __del__(self):
            self.fligh.close()
            self.account.close()
            self.hotel.close()

#--------------------BEGIN------------------------
if __name__ == '__main__':
    databaseConnection  = DatabaseConnection()
    databaseConnection.bookFlight()
#    bookFlight(con1, con3)

#con1.close()
#con2.close()
#con3.close()
