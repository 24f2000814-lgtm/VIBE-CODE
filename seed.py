from app import app, db
from models import Flight, User
from datetime import datetime, timedelta
import random

def seed_data():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Seed Users
        users = [
            User(name='John Doe', email='john.doe@example.com', phone_number='1234567890'),
            User(name='Jane Smith', email='jane.smith@example.com', phone_number='0987654321')
        ]
        db.session.bulk_save_objects(users)
        db.session.commit()

        # Seed Flights
        airlines = ['American Airlines', 'Delta', 'United', 'Southwest', 'Alaska']
        cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']

        for _ in range(50):
            origin = random.choice(cities)
            destination = random.choice(list(set(cities) - {origin}))
            departure_time = datetime.now() + timedelta(days=random.randint(1, 30), hours=random.randint(0, 23), minutes=random.randint(0, 59))
            duration = random.randint(1, 10)
            arrival_time = departure_time + timedelta(hours=duration)

            flight = Flight(
                flight_number=''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6)),
                airline=random.choice(airlines),
                origin=origin,
                destination=destination,
                departure_time=departure_time,
                arrival_time=arrival_time,
                duration=duration * 60,
                price=round(random.uniform(100, 1000), 2),
                available_seats=random.randint(0, 200)
            )
            db.session.add(flight)
        db.session.commit()

if __name__ == '__main__':
    seed_data()
