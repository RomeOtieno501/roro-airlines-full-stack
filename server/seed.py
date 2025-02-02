from models import db, Airline, Flight, Passenger, Booking, Seat
from app import app
from datetime import datetime, timedelta

# Clear existing data 
def clear_database():
    db.session.query(Airline).delete()
    db.session.query(Flight).delete()
    db.session.query(Passenger).delete()
    db.session.query(Booking).delete()
    db.session.query(Seat).delete()
    db.session.commit()

def seed_database():
    # Create sample airlines
    airline1 = Airline(name="Kenya Airways", country="Kenya")
    airline2 = Airline(name="Dutch Airlines", country="Netherlands")
    airline3 = Airline(name="Turkish Airlines", country="Turkey")

    db.session.add_all([airline1, airline2, airline3])
    db.session.commit()

    # Create sample flights
    flight1 = Flight(airline_id=airline1.id, departure_time=datetime.now() + timedelta(days=1),
                     arrival_time=datetime.now() + timedelta(days=1, hours=5), origin="Kenya", destination="London")
    flight2 = Flight(airline_id=airline2.id, departure_time=datetime.now() + timedelta(days=2),
                     arrival_time=datetime.now() + timedelta(days=2, hours=6), origin="Netherlands", destination="Kenya")
    flight3 = Flight(airline_id=airline3.id, departure_time=datetime.now() + timedelta(days=3),
                     arrival_time=datetime.now() + timedelta(days=3, hours=7), origin="Turkey", destination="Kenya")
    
    db.session.add_all([flight1, flight2, flight3])
    db.session.commit()

    # Create sample passengers
    passenger1 = Passenger(name="Rome Otieno", email="otienorome2@gmail.com")
    passenger2 = Passenger(name="Lavine Onyango", email="lonyango5@gmail.com")
    passenger3 = Passenger(name="Treva Odhiambo", email="trevaodhiambo45@gmail.com")
    
    db.session.add_all([passenger1, passenger2, passenger3])
    db.session.commit()

    # Create sample bookings
    booking1 = Booking(passenger_id=passenger1.id, booking_date=datetime.now())
    booking2 = Booking(passenger_id=passenger2.id, booking_date=datetime.now())
    booking3 = Booking(passenger_id=passenger3.id, booking_date=datetime.now())
    
    db.session.add_all([booking1, booking2, booking3])
    db.session.commit()

    # Create sample seats
    seat1 = Seat(flight_id=flight1.id, seat_number="12A", is_booked=True, booking_id=booking1.id)
    seat2 = Seat(flight_id=flight2.id, seat_number="15B", is_booked=True, booking_id=booking2.id)
    seat3 = Seat(flight_id=flight3.id, seat_number="18C", is_booked=True, booking_id=booking3.id)
    
    db.session.add_all([seat1, seat2, seat3])
    db.session.commit()
    
    print("Database seeded successfully!")

if __name__ == "__main__":
    with app.app_context():
        print("Clearing database...")
        clear_database()
        print("Seeding database...")
        seed_database()
