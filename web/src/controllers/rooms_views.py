from datetime import datetime
from flask import render_template, request, session

from src import db
from src.models.models import Attendant, Room, Rent
from src.utils.decorators import login_required

@login_required
def rooms():
    rooms = Room.query.order_by(Room.room_number).all()
    attendant = Attendant.query.filter(Attendant.email == session['email']).first()
    if request.method == 'POST':
        room_number_day = request.form['reservarion']
        room_number, day = room_number_day.split('&')
        rent = Rent(int(room_number), attendant.att_id, datetime(day=int(day), year=2023, month=6))
        db.session.add(rent)
        db.session.commit()
    return render_template('room_list.html', rooms = rooms)