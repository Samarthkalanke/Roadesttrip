import datetime
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.reservations import Reservations

reservations_api = Blueprint('reservations_api', __name__,
                   url_prefix='/api/reservations')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(reservations_api)

class ReservationsAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            #print("this is the body")
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate LicensePlate
            LicensePlate = body.get('LicensePlate')
            if LicensePlate is None or len(LicensePlate) < 2:
                return {'message': f'LicensePlate is missing, or is less than 2 characters'}, 210
            # look for person and date of reservation
            person = body.get('person')
            ReservationDate = body.get('ReservationDate')

            ''' #1: Key code block, setup USER OBJECT '''
            uo = Reservations(car=car, 
                      reservationid=reservationid)
            
            ''' Additional garbage error checking '''
            # set password if provided
            if person is not None:
                uo.set_person(person)
            # convert to date type
            if ReservationDate is not None:
                try:
                    current_datetime = datetime.datetime.now()
                    uo.Set_ReservationDate = current_datetime.strftime("%d-%m-%Y")
                   # uo.ReservationDate = datetime.strptime(ReservationDate, '%Y-%m-%d').date()
                except:
                    return {'message': f'Invalid reservation date'}, 210
            
            ''' #2: Key Code block to add user to database '''
            # create user in databaseF
            reservation = uo.create()
            # success returns json of user
            if reservation:
                return jsonify(reservation.read())
            # failure returns error
            return {'message': f'Processed {car}, either a format error or reservation ID {reservationid} is duplicate'}, 210

    class _Read(Resource):
        def get(self):
            allReservations = Reservations.query.all()    # read/extract all users from database
            json_ready = [myReservation.read() for myReservation in allReservations]  # prepare output in json #json_ready = [user.read() for user in users]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')