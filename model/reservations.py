""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash



reservation_data = []
cars_list = [
    "Tesla",
    "Mini",
    "Ford",
    "Toyota",
    "Honda"
]

# Initialize reservations
def initReservations():
    # setup reservations into a dictionary
    item_id = 0
    for item in cars_list:
        reservation_data.append({"reservationid": str(item_id), "car": item, "LicensePlate": str(item_id), "person": "Person"+str(item_id + 1), "ReservationDate": "12/12/2023"})
        item_id += 1
    #pass
     
# Return all reservations
def getReservations():
    return(reservation_data)


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the Post class to manage actions in 'Reservations' table
class Post2(db.Model):
    __tablename__ = 'reservations'

    # Define the reservation schema
    reservationid = db.Column(db.String, primary_key=True)
    car = db.Column(db.String, unique=False, nullable=False)
    LicensePlate = db.Column(db.String, unique=False)
    person = db.Column(db.String, unique=False)
    ReservationDate = db.Column(db.String, unique=False)

    # Constructor of a Reservation object, initializes of instance variables within object
    def __init__(self, reservationid, car, LicensePlate, person, ReservationDate):
        self.reservatonid = reservationid
        self.car = car
        self.LicensePlate = LicensePlate
        self.person = person
        self.ReservationDate = ReservationDate

    # Returns a string representation of the Reservation object, similar to java toString()
    # returns string
    def __repr__(self):
        return ("reservations(" + 
                str(self.reservatonid) + 
                "," + str(self.car) + 
                "," + str(self.LicensePlate) + "," + str(self.person) +"," + str(self.ReservationDate))

    # CRUD create, adds a new record to the Notes table
    # returns the object added or None in case of an error
    def create(self):
        try:
            # creates a Notes object from Notes(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Notes table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read, returns dictionary representation of Notes object
    # returns dictionary
    def read(self):
        # encode image
        # path = app.config['UPLOAD_FOLDER']
        # file = os.path.join(path, self.image)
        # file_text = open(file, 'rb')
        # file_read = file_text.read()
        # file_encode = base64.encodebytes(file_read)
        
        return {
            "reservationid": self.reservationid,
            "car": self.car,
            "LicensePlate": self.LicensePlate,
            "person": self.person,
            "ReservationDate": self.ReservationDate
        }
    # CRUD update: updates user name, password, phone
    # returns self
    '''def update(self, reservationid="", person="", ReservationDate=""):
        """only updates values with length"""
        if len(person) > 0:
            self.person = person
        if len(reservationid) > 0:
            self.reservationid = reservationid
        if len(ReservationDate) > 0:
            self.ReservationDate = ReservationDate
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None'''

class Reservations(db.Model):
    __tablename__ = "carreservations"

    reservationid = db.Column(db.Integer, primary_key=True)
    car = db.Column(db.String)
    LicensePlate = db.Column(db.String)
    person = db.Column(db.String)
    ReservationDate = db.Column(db.String)

    def __init__(self, reservationid, car, LicensePlate, person, ReservationDate):
  
        self.reservatonid = reservationid
        self.car = car
        self.LicensePlate = LicensePlate
        self.person = person
        self.ReservationDate = ReservationDate

    @property
    def name(self):
         return {
            self.reservationid,
            self.car,
            self.LicensePlate,
            self.person,
            self.ReservationDate
         }
    
    ##a setter function, allows name to be updated after initial object creation
    #@car.setter
     #def name(self, name):
         # self.car = car
    
   
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())


    def read(self):
        return {
            "reservationid": self.reservationid,
            "car": self.car,
            "LicensePlate": self.LicensePlate,
            "person": self.person,
            "ReservationDate": self.ReservationDate
        }
    
    def create(self):
        try:
            # creates a Notes object from Notes(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Notes table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

"""Database Creation and Testing """


# Builds working data for testing
def initReservation():
    with app.app_context():
        """Create database and tables"""
        db.init_app(app)
        db.create_all()
        """Tester data for table"""
        r1 = Reservations(reservationid='125', car ='Tesla', LicensePlate = '12345', person = 'MYName1', ReservationDate = '2/23/2023') 
        r2 = Reservations(reservationid='124', car ='TeslaX', LicensePlate = '23456', person = 'MYName2', ReservationDate = '2/23/2023') 
        #User(name='John Smith', uid='Ford Taurus', password='3/9-3/12')
        #u2 = User(name='Trent Cardall', uid='Buick Enclave', password='3/13')

        reservations = [r1, r2]
        #reservations.posts.append

        """Builds sample user/note(s) data"""
        for reservation in reservations:
            try:
                '''add a few 1 to 4 notes per user'''
                for num in range(randrange(1, 4)):
                    note = "#### " + reservation.car + " car " + str(num) + ". \n Generated by test data."
                    reservation.posts.append(Post2(reservationid=reservation.reservationid, car=reservation.car, LicensePlate=reservation.LicensePlate, person = reservation.person, ReservationDate = reservation.ReservationDate))
                '''add user/post data to table'''
                reservation.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {reservation.reservationid}")
            