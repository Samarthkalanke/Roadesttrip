import random

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
     
# Return all reservations
def getReservations():
    return(reservation_data)


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the Post class to manage actions in 'Reservations' table
class Reservations(db.Model):
    __tablename__ = 'reservations'

    # Define the reservation schema
    reservationid = db.Column(db.Integer, primary_key=True)
    car = db.Column(db.String, unique=False, nullable=False)
    LicensePlate = db.Column(db.String, unique=False)
    person = db.Column(db.String, unique=False)
  #  ReservationDate = db.Colunmn(db.text, unique=False)

    # Constructor of a Reservation object, initializes of instance variables within object
    def __init__(self, reservationid, car, LicensePlate, person, ReservationDate):
        self.reservatonid = reservationid
        self.car = car
        self.LicensePlate = LicensePlate
        self.person = person
        self.ReservationDate = ReservationDate


    # @property
    # def name(self):
    #     return self._name
    
    # # a setter function, allows name to be updated after initial object creation
    # @name.setter
    # def name(self, name):
    #     self._name = name
    
    # # a getter method, extracts email from object
    # @property
    # def uid(self):
    #     return self._uid
    
    # # a setter function, allows name to be updated after initial object creation
    # @uid.setter
    # def uid(self, uid):
    #     self._uid = uid
        
    # # check if uid parameter matches user id in object, return boolean
    # def is_uid(self, uid):
    #     return self._uid == uid
    
    # @property
    # def password(self):
    #     return self._password

    # # update password, this is conventional setter
    # def set_password(self, password):
    #     """Create a hashed password."""
    #     self._password = password
    
    # # dob property is returned as string, to avoid unfriendly outcomes
    # @property
    # def dob(self):
    #     dob_string = self._dob.strftime('%m-%d-%Y')
    #     return dob_string
    
    # # dob should be have verification for type date
    # @dob.setter
    # def dob(self, dob):
    #     self._dob = dob
    
    # @property
    # def age(self):
    #     today = date.today()
    #     return today.year - self._dob.year - ((today.month, today.day) < (self._dob.month, self._dob.day))
   

    # Returns a string representation of the Reservation object, similar to java toString()
    # returns string
    def __repr__(self):
        return ("Reservations(" + 
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
        path = app.config['UPLOAD_FOLDER']
        file = os.path.join(path, self.image)
        file_text = open(file, 'rb')
        file_read = file_text.read()
        file_encode = base64.encodebytes(file_read)
        
        return {
            "reservationId": self.reservatonid,
            "car": self.car,
            "LicensePlate": self.LicensePlate,
            "person": self.person,
            "ReservationDate": self.ReservationDate
        }
    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, reservationid="", person="", ReservationDate=""):
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
        return None

# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
# class Reservations(db.Model):
#     __tablename__ = 'users'  # table name is plural, class name is singular

#     Define the User schema with "vars" from object
#     id = db.Column(db.Integer, primary_key=True)
#     _name = db.Column(db.String(255), unique=False, nullable=False)
#     _uid = db.Column(db.String(255), unique=True, nullable=False)
#     _password = db.Column(db.String(255), unique=False, nullable=False)
#     _dob = db.Column(db.Date)

#     Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
#     posts = db.relationship("Post", cascade='all, delete', backref='users', lazy=True)

#     constructor of a User object, initializes the instance variables within object (self)
#     def __init__(self, name, uid, password="123qwerty", dob=date.today()):
#         self._name = name    # variables with self prefix become part of the object, 
#         self._uid = uid
#         self.set_password(password)
#         self._dob = dob

#     a name getter method, extracts name from object
#     @property
#     def name(self):
#         return self._name
    
#     a setter function, allows name to be updated after initial object creation
#     @name.setter
#     def name(self, name):
#         self._name = name
    
#     a getter method, extracts email from object
#     @property
#     def uid(self):
#         return self._uid
    
#     a setter function, allows name to be updated after initial object creation
#     @uid.setter
#     def uid(self, uid):
#         self._uid = uid
        
#     check if uid parameter matches user id in object, return boolean
#     def is_uid(self, uid):
#         return self._uid == uid
    
#     @property
#     def password(self):
#         return self._password

#     update password, this is conventional setter
#     def set_password(self, password):
#         """Create a hashed password."""
#         self._password = password
    
#     dob property is returned as string, to avoid unfriendly outcomes
#     @property
#     def dob(self):
#         dob_string = self._dob.strftime('%m-%d-%Y')
#         return dob_string
    
#     dob should be have verification for type date
#     @dob.setter
#     def dob(self, dob):
#         self._dob = dob
    
#     @property
#     def age(self):
#         today = date.today()
#         return today.year - self._dob.year - ((today.month, today.day) < (self._dob.month, self._dob.day))
    
#     output content using str(object) in human readable form, uses getter
#     output content using json dumps, this is ready for API response
#     def __str__(self):
#         return json.dumps(self.read())

#     CRUD create/add a new record to the table
#     returns self or None on error
#     def create(self):
#         try:
#             creates a person object from User(db.Model) class, passes initializers
#             db.session.add(self)  # add prepares to persist person object to Users table
#             db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
#             return self
#         except IntegrityError:
#             db.session.remove()
#             return None

#     CRUD read converts self to dictionary
#     returns dictionary
#     def read(self):
#         return {
#             "id": self.id,
#             "name": self.name,
#             "uid": self.uid,
#             "dob": self.dob,
#             "age": self.age,
#             "posts": [post.read() for post in self.posts]
#         }

#     CRUD update: updates user name, password, phone
#     returns self
#     def update(self, name="", uid="", password=""):
#         """only updates values with length"""
#         if len(name) > 0:
#             self.name = name
#         if len(uid) > 0:
#             self.uid = uid
#         if len(password) > 0:
#             self.set_password(password)
#         db.session.commit()
#         return self

#     CRUD delete: remove self
#     None
#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()
#         return None


"""Database Creation and Testing """


# Builds working data for testing
def initReservation():
    with app.app_context():
        """Create database and tables"""
        db.init_app(app)
        db.create_all()
        """Tester data for table"""
        r1 = Reservation(reservationid='123', car ='Tesla', LicensePlate = '12345', person = 'MYName1', ReservationDate = '2/23/2023') 
        r2 = Reservation(reservationid='124', car ='TeslaX', LicensePlate = '23456', person = 'MYName2', ReservationDate = '2/23/2023') 
        #User(name='John Smith', uid='Ford Taurus', password='3/9-3/12')
        #u2 = User(name='Trent Cardall', uid='Buick Enclave', password='3/13')

        reservations = [r1, r2]
        #reservations.posts.append

        """Builds sample user/note(s) data"""
        # for reservation in reservations:
        #     try:
        #         '''add a few 1 to 4 notes per user'''
        #         for num in range(randrange(1, 4)):
        #             note = "#### " + user.name + " note " + str(num) + ". \n Generated by test data."
        #             user.posts.append(Post(id=user.id, note=note, image='ncs_logo.png'))
        #         '''add user/post data to table'''
        #         user.create()
        #     except IntegrityError:
        #         '''fails with bad or duplicate data'''
        #         db.session.remove()
        #         print(f"Records exist, duplicate email, or error: {user.uid}")
            