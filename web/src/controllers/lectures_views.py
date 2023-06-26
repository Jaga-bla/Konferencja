from datetime import datetime
from flask import render_template, request, redirect, session, flash

from src import db
from src.models.models import Lecture, Attendant
from src.utils.decorators import login_required

def lectures():
    lectures = Lecture.query.order_by(Lecture.date).all()
    return render_template('lectures_list.html', lectures = lectures)

@login_required
def add_lecture():
    dates = []
    attendant = Attendant.query.filter(Attendant.email == session['email']).first()
    for date in range(26,31):
        for hour in range(8,15):
            new_date = datetime(year=2023, month=6, day=date, hour=hour)
            if Lecture.query.filter(Lecture.date==new_date).first() == None:
                dates.append(datetime(year=2023, month=6, day=date, hour=hour))
    if request.method == 'POST':
        name = request.form['name']
        att_id = attendant.att_id
        date = request.form.get('date')
        datetime_value = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        lecture = Lecture(att_id, name, datetime_value)
        db.session.add(lecture)
        db.session.commit()
        return redirect("/prezentacje", code=302)
    return render_template('lecture_form.html', dates=dates)

@login_required
def edit_lecture(lecture_id):
    lecture = Lecture.query.get_or_404(lecture_id)
    attendant = Attendant.query.filter(Attendant.email == session['email']).first()
    if lecture.att_id != attendant.att_id:
        flash("Nie jesteś autorem.")
        return redirect("/prezentacje")
    dates = []
    for date in range(26,31):
        for hour in range(8,15):
            new_date = datetime(year=2023, month=6, day=date, hour=hour)
            if Lecture.query.filter(Lecture.date==new_date).first() == None:
                dates.append(datetime(year=2023, month=6, day=date, hour=hour))
    if request.method == 'GET':
        lecture = {
            "lecture_id" : lecture.lecture_id,
            "name": lecture.name,
            "date": lecture.date
        }
        return render_template('lecture_update.html', lecture=lecture, dates=dates)

    elif request.method == 'POST':
        lecture.att_id = request.form.get('att_id', lecture.att_id)
        lecture.name = request.form.get('name', lecture.name)
        if not lecture.date == request.form.get('date', lecture.date):
            lecture.date = request.form.get('date')
        db.session.commit()
        
        return redirect("/prezentacje", code=302)