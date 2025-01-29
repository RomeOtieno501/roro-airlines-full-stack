from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime


metadata = MetaData()

# Initialize SQLAlchemy
db = SQLAlchemy(metadata=metadata)


# Airline model
class Airline(db.Model):
    __tablename__ = 'airline'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50), nullable=False)

    flights = db.relationship('Flight', back_populates='airline', lazy=True)

    # def __repr__(self):
    #     return f'Airline {self.name} from {self.country} country with id {self.id}'


# Flight model
class Flight(db.Model):
    __tablename__ = 'flights'

    id = db.Column(db.Integer, primary_key=True)
    airline_id = db.Column(db.Integer, db.ForeignKey('airline.id'), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    origin = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)

    seat = db.relationship('Seat', back_populates='flights', lazy=True)
    airline = db.relationship('Airline', back_populates='flights', lazy=True)

    # def __repr__(self):
    #     return f'Flight from {self.origin} to {self.destination} by airline {self.airline_id}'

# Passenger model
class Passenger(db.Model):
    __tablename__ = 'passenger'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

    bookings = db.relationship('Booking', back_populates='passenger', lazy=True)

    # def __repr__(self):
    #     return f'Passenger {self.name} with email {self.email}'

# Booking model
class Booking(db.Model):
    __tablename__ = 'booking'

    id = db.Column(db.Integer, primary_key=True)
    passenger_id = db.Column(db.Integer, db.ForeignKey('passenger.id'), nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False, default=datetime.now)

    seat = db.relationship('Seat', back_populates='booking', uselist=False)  # One-to-one relationship with Seat
    passenger = db.relationship('Passenger', back_populates='bookings', lazy=True)

    # def __repr__(self):
    #     return f'Booking for passenger {self.passenger_id} on {self.booking_date}'

# Seat model
class Seat(db.Model):
    __tablename__ = 'seat'

    id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'), nullable=False)
    seat_number = db.Column(db.String(10), nullable=False)
    is_booked = db.Column(db.Boolean, default=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), unique=True, nullable=True)
    
    flights = db.relationship('Flight', back_populates='seat', lazy=True)      
    booking = db.relationship('Booking', back_populates='seat', uselist=False)  # One-to-one relationship with Booking

    # def __repr__(self):
    #     return f'Seat {self.seat_number} for flight {self.flight_id} is booked: {self.is_booked}'