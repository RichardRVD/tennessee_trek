from crypt import methods
from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.trip import Trip

@app.route('/create/trip', methods=['POST'])
def create_trip():
    data = {
        'name' : request.form['name'],
        'description' : request.form['description'],
        'price' : request.form['price'],
        'date' : request.form['date'],
        'time' : request.form['time'],
        'order_id' : request.form['order_id']
    }
    data = Trip.create_trip(data)
    return redirect('/book')

@app.route('/book')
def show_all_trips():
    trips = Trip.get_all_trips()
    return render_template('/book',trips=trips)

