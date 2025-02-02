from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db
from flask_restful import Api, Resource
from models import Airline, Flight, Passenger, Booking, Seat
from datetime import datetime
from flask_cors import CORS
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

def convert_to_datetime(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return None


# Flask-RESTful Resources
class HomeResource(Resource):
    def get(self):
        return {"message": "Welcome to the Airlines API!"}, 200

api.add_resource(HomeResource, "/")


class AirlineResource(Resource):
    def get(self):
        airlines = Airline.query.all()
        return [
            {"id": airline.id, "name": airline.name, "country": airline.country}
            for airline in airlines
        ], 200

    def post(self):
        data = request.get_json()  
        if not data or "name" not in data or "country" not in data:
            return {"error": "Missing 'name' or 'country' field"}, 400 

        new_airline = Airline(name=data["name"], country=data["country"])
        db.session.add(new_airline)
        db.session.commit()

        return {
            "message": "Airline created",
            "id": new_airline.id,
            "name": new_airline.name,
            "country": new_airline.country
        }, 201 

    def put(self, id):
        airline = Airline.query.get(id)
        if not airline:
            return {"error": "Airline not found"}, 404

        data = request.get_json()
        for field in ["name", "country"]:
            if field in data:
                setattr(airline, field, data[field])

        db.session.commit()
        return {"message": "Airline updated", "id": airline.id}, 200

    def delete(self, id):
        airline = Airline.query.get(id)
        if not airline:
            return {"error": "Airline not found"}, 404

        db.session.delete(airline)
        db.session.commit()
        return {"message": "Airline deleted"}, 200

api.add_resource(AirlineResource, "/airlines", "/airlines/<int:id>")


class FlightResource(Resource):
    def get(self):
        flights = Flight.query.all()
        return [
            {
                "id": flight.id,
                "airline_id": flight.airline_id,
                "departure_time": flight.departure_time.strftime('%Y-%m-%dT%H:%M:%S') if flight.departure_time else None,
                "arrival_time": flight.arrival_time.strftime('%Y-%m-%dT%H:%M:%S') if flight.arrival_time else None,
                "origin": flight.origin,
                "destination": flight.destination,
            }
            for flight in flights
        ], 200

    def post(self):
        data = request.get_json()
        required_fields = ["airline_id", "departure_time", "arrival_time", "origin", "destination"]
        
        if not all(field in data for field in required_fields):
            return {"error": "Missing required fields"}, 400

        # Convert datetime strings to datetime objects
        departure_time = convert_to_datetime(data["departure_time"])
        arrival_time = convert_to_datetime(data["arrival_time"])
        
        if not departure_time or not arrival_time:
            return {"error": "Invalid datetime format. Use YYYY-MM-DDTHH:MM:SS"}, 400
        
        if departure_time >= arrival_time:
            return {"error": "Arrival time must be later than departure time"}, 400
        
        new_flight = Flight(
            airline_id=data["airline_id"],
            departure_time=departure_time,
            arrival_time=arrival_time,
            origin=data["origin"],
            destination=data["destination"]
        )

        db.session.add(new_flight)
        db.session.commit()

        return {
            "message": "Flight created",
            "id": new_flight.id,
            "airline_id": new_flight.airline_id,
            "departure_time": new_flight.departure_time.strftime('%Y-%m-%dT%H:%M:%S'),
            "arrival_time": new_flight.arrival_time.strftime('%Y-%m-%dT%H:%M:%S'),
            "origin": new_flight.origin,
            "destination": new_flight.destination
        }, 201

    def put(self, id):
        flight = Flight.query.get(id)
        if not flight:
            return {"error": "Flight not found"}, 404

        data = request.get_json()
        
        if 'departure_time' in data:
            data['departure_time'] = convert_to_datetime(data['departure_time']) if isinstance(data['departure_time'], str) else data['departure_time']
        if 'arrival_time' in data:
            data['arrival_time'] = convert_to_datetime(data['arrival_time']) if isinstance(data['arrival_time'], str) else data['arrival_time']

        for field in ["airline_id", "departure_time", "arrival_time", "origin", "destination"]:
            if field in data:
                setattr(flight, field, data[field])

        db.session.commit()
        return {"message": "Flight updated", "id": flight.id}, 200

    def delete(self, id):
        flight = Flight.query.get(id)
        if not flight:
            return {"error": "Flight not found"}, 404

        db.session.delete(flight)
        db.session.commit()
        return {"message": "Flight deleted"}, 200

    
api.add_resource(FlightResource, "/flights", "/flights/<int:id>")


class PassengerResource(Resource):
    def get(self):
        passengers = Passenger.query.all()
        return [
            {"id": p.id, "name": p.name, "email": p.email}
            for p in passengers
        ], 200

    def post(self):
        data = request.get_json()
        if not data or "name" not in data or "email" not in data:
            return {"error": "Missing 'name' or 'email' field"}, 400

        new_passenger = Passenger(**data)
        db.session.add(new_passenger)
        db.session.commit()

        return {
            "message": "Passenger created",
            "id": new_passenger.id,
            "name": new_passenger.name,
            "email": new_passenger.email
        }, 201

    def put(self, id):
        passenger = Passenger.query.get(id)
        if not passenger:
            return {"error": "Passenger not found"}, 404

        data = request.get_json()
        for field in ["name", "email"]:
            if field in data:
                setattr(passenger, field, data[field])

        db.session.commit()
        return {"message": "Passenger updated", "id": passenger.id}, 200

    def delete(self, id):
        passenger = Passenger.query.get(id)
        if not passenger:
            return {"error": "Passenger not found"}, 404

        db.session.delete(passenger)
        db.session.commit()
        return {"message": "Passenger deleted"}, 200

api.add_resource(PassengerResource, "/passengers", "/passengers/<int:id>")


class BookingResource(Resource):
    def get(self):
        bookings = Booking.query.all()
        return [
            {
                "id": b.id,
                "passenger_id": b.passenger_id,
                "booking_date": b.booking_date.strftime('%Y-%m-%dT%H:%M:%S') if b.booking_date else None
            }
            for b in bookings
        ], 200

    def post(self):
        data = request.get_json()
        if not data or "passenger_id" not in data or "booking_date" not in data:
            return {"error": "Missing 'passenger_id' or 'booking_date' field"}, 400

        booking_date = convert_to_datetime(data["booking_date"])
        if not booking_date:
            return {"error": "Invalid datetime format. Use YYYY-MM-DDTHH:MM:SS"}, 400

        new_booking = Booking(
            passenger_id=data["passenger_id"],
            booking_date=booking_date
        )
        db.session.add(new_booking)
        db.session.commit()

        return {
            "message": "Booking created",
            "id": new_booking.id,
            "passenger_id": new_booking.passenger_id,
            "booking_date": new_booking.booking_date.strftime('%Y-%m-%dT%H:%M:%S')
        }, 201

    def put(self, id):
        booking = Booking.query.get(id)
        if not booking:
            return {"error": "Booking not found"}, 404

        data = request.get_json()
        if 'booking_date' in data:
            data['booking_date'] = convert_to_datetime(data['booking_date']) if isinstance(data['booking_date'], str) else data['booking_date']

        for field in ["passenger_id", "booking_date"]:
            if field in data:
                setattr(booking, field, data[field])

        db.session.commit()
        return {"message": "Booking updated", "id": booking.id}, 200

    def delete(self, id):
        booking = Booking.query.get(id)
        if not booking:
            return {"error": "Booking not found"}, 404

        db.session.delete(booking)
        db.session.commit()
        return {"message": "Booking deleted"}, 200
    

api.add_resource(BookingResource, "/bookings", "/bookings/<int:id>")


class SeatResource(Resource):
    def get(self):
        seats = Seat.query.all()
        return [
            {
                "id": seat.id,
                "flight_id": seat.flight_id,
                "seat_number": seat.seat_number,
                "is_booked": seat.is_booked,
                "booking_id": seat.booking_id,
            }
            for seat in seats
        ], 200

    def post(self):
        data = request.get_json()
        required_fields = ["flight_id", "seat_number", "is_booked", "booking_id"]
        
        if not all(field in data for field in required_fields):
            return {"error": "Missing required fields"}, 400

        new_seat = Seat(**data)
        db.session.add(new_seat)
        db.session.commit()

        return {
            "message": "Seat created",
            "id": new_seat.id,
            "flight_id": new_seat.flight_id,
            "seat_number": new_seat.seat_number,
            "is_booked": new_seat.is_booked,
            "booking_id": new_seat.booking_id
        }, 201

    def put(self, id):
        seat = Seat.query.get(id)
        if not seat:
            return {"error": "Seat not found"}, 404

        data = request.get_json()
        for field in ["flight_id", "seat_number", "is_booked", "booking_id"]:
            if field in data:
                setattr(seat, field, data[field])

        db.session.commit()
        return {"message": "Seat updated", "id": seat.id}, 200

    def delete(self, id):
        seat = Seat.query.get(id)
        if not seat:
            return {"error": "Seat not found"}, 404

        db.session.delete(seat)
        db.session.commit()
        return {"message": "Seat deleted"}, 200
    
api.add_resource(SeatResource, "/seats")


if __name__ == '__main__':
    app.run(debug=True, port=5555)