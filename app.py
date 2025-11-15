from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import random
import string
from datetime import datetime
from models import db, Flight, User, Booking

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flights.db'
app.config['SECRET_KEY'] = 'dev'
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    departure_city = request.form['departure_city']
    destination_city = request.form['destination_city']
    departure_date = datetime.strptime(request.form['departure_date'], '%Y-%m-%d').date()
    return_date = request.form.get('return_date')

    flights = Flight.query.filter(
        Flight.origin == departure_city,
        Flight.destination == destination_city,
        db.func.date(Flight.departure_time) == departure_date
    ).all()

    return_flights = []
    if return_date:
        return_date = datetime.strptime(return_date, '%Y-%m-%d').date()
        return_flights = Flight.query.filter(
            Flight.origin == destination_city,
            Flight.destination == departure_city,
            db.func.date(Flight.departure_time) == return_date
        ).all()

    airlines = list(set([flight.airline for flight in flights] + [flight.airline for flight in return_flights]))

    return render_template('results.html', flights=flights, return_flights=return_flights, airlines=airlines)

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        flight_id = request.form['flight_id']
    else:
        flight_id = request.args.get('flight_id')
    flight = Flight.query.get(flight_id)
    return render_template('book.html', flight=flight)

@app.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    flight_id = request.form['flight_id']
    flight = Flight.query.get(flight_id)
    seats_booked = int(request.form['seats'])

    if flight.available_seats >= seats_booked:
        # Simulate payment
        payment_successful = random.choice([True, False])

        if payment_successful:
            user = User.query.filter_by(email=request.form['email']).first()
            if not user:
                user = User(
                    name=request.form['name'],
                    email=request.form['email'],
                    phone_number=request.form['phone_number']
                )
                db.session.add(user)
                db.session.commit()

            booking_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            booking = Booking(
                booking_id=booking_id,
                user_id=user.id,
                flight_id=flight.id,
                seats_booked=seats_booked
            )
            flight.available_seats -= seats_booked
            db.session.add(booking)
            db.session.commit()

            return render_template('confirmation.html', booking=booking)
        else:
            flash('Payment failed. Please try again.')
            return redirect(url_for('book', flight_id=flight_id))
    else:
        flash('Not enough seats available.')
        return redirect(url_for('book', flight_id=flight_id))

@app.route('/login', methods=['POST'])
def login():
    user = User.query.filter_by(email=request.form['email']).first()
    if user:
        session['user_id'] = user.id
        return redirect(url_for('booking_history'))
    else:
        flash('User not found.')
        return redirect(url_for('index'))

@app.route('/booking_history')
def booking_history():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template('history.html', bookings=user.bookings)
    else:
        flash('Please login to view your booking history.')
        return redirect(url_for('index'))

@app.route('/cancel_booking', methods=['POST'])
def cancel_booking():
    booking_id = request.form['booking_id']
    booking = Booking.query.get(booking_id)
    booking.flight.available_seats += booking.seats_booked
    booking.booking_status = 'Cancelled'
    db.session.commit()
    return redirect(url_for('booking_history'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)