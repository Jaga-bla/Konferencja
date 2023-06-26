from datetime import date

from flask import render_template, request, redirect, flash
from sqlalchemy import desc

from src import db
from src.models.models import Attendant, University, Room, Rent
from src.utils.decorators import login_required, admin_only


@login_required
@admin_only
def analytics():
    academic_title = db.session.query(Attendant.academic_title, db.func.count(Attendant.academic_title)).group_by(
        Attendant.academic_title).order_by(desc(db.func.count(Attendant.academic_title))).all()
    
    average_cost = db.session.query(db.func.avg(Attendant.costs)).scalar()
    
    tour = db.session.query(db.func.count(Attendant.is_tour)).filter(Attendant.is_tour == True).scalar()

    banquet = db.session.query(db.func.count(Attendant.is_banquet)).filter(Attendant.is_banquet == True).scalar() 
          
    data = {
        'most_academic_title':academic_title,
        'average_cost': round(average_cost,2),
        'tour': tour,
        'banquet': banquet,
        'monday':20-get_available_rooms_no(date(2023,6,26)),
        'thuesday':20-get_available_rooms_no(date(2023,6,27)),
        'wednesday':20-get_available_rooms_no(date(2023,6,28)),
        'thursday':20-get_available_rooms_no(date(2023,6,29)),
        'friday':20-get_available_rooms_no(date(2023,6,30))
    }
    return render_template('analytics.html', data=data)

def get_available_rooms_no(date):
    return db.session.query(db.func.count(Room.room_number)).outerjoin(
    Rent, Room.room_number == Rent.room_number).filter(Rent.date == date).scalar()

@login_required
@admin_only
def attendants_list():
    attendants = Attendant.query.order_by(Attendant.att_id).all()
    universities = University.query.all()
    if request.method == 'POST':
        att_id = request.form.get('att_id')
        if att_id:
            attendant = Attendant.query.get(att_id)
            db.session.delete(attendant)
            db.session.commit()
            flash("Usunięto uczestnika.")
            
        univ_id = request.form.get('univ_id')
        if univ_id:
            university = University.query.get(univ_id)
            db.session.delete(university)
            db.session.commit()
            flash("Usunięto uniwersytet.")
        return redirect("/lista/uczestnikow", code=302)
    return render_template('attendants_list.html', attendants=attendants, universities=universities)