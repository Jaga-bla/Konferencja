from flask import render_template, request, redirect, session, flash

from src import db, bcrypt
from src.models.models import Attendant, University
from src.utils.forms import attendant_form
from src.utils.decorators import login_required, admin_only

def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        attendant = Attendant.query.filter(Attendant.email==email).first()
        if attendant and bcrypt.check_password_hash(attendant.password, password):
            session['email'] = attendant.email
            return redirect('/prezentacje')
        else:
            flash("Nieprawidłowy email lub hasło")
    return render_template('login.html')

def logout():
    session.pop('email', default = None)
    flash("Wylogowano.")
    return redirect('/prezentacje')

def registration():
    universities = University.query.all()
    if request.method == 'POST':
        try:
            attendant = attendant_form(request.form)
        except ValueError as e:
            flash("Nieprawidłowe dane")
            return render_template('registration.html', universities=universities)
        password = request.form.get('password')
        attendant.password = bcrypt.generate_password_hash(password).decode('utf-8')
        univ = request.form.get('univ_name')

        if univ !="":
            univ = University.query.get(univ)
            attendant.universities.append(univ)
        session['email']=attendant.email
        db.session.add(attendant)

        db.session.commit()
        
        return redirect("/prezentacje", code=302)
    return render_template('registration.html', universities=universities)

@login_required
def edit_attendant(att_id):
    attendant = Attendant.query.get_or_404(att_id)
    universities = University.query.all()
    if request.method == 'GET':
        attendant = {
            "fname": attendant.fname,
            "lname": attendant.lname,
            "email": attendant.email,
            "academic_title":attendant.academic_title,
            "is_banquet":attendant.is_banquet,
            "is_tour":attendant.is_tour,
            "universities": attendant.universities
        }
        return render_template('attendant_update.html', attendant=attendant, universities=universities)

    elif request.method == 'POST':
        attendant = attendant_form(request.form, attendant=attendant)
        
        univ = request.form.get('univ_name')
            

        if univ !="":
            univ = University.query.get(univ)
            attendant.universities.append(univ)

        db.session.commit()
        
        return redirect("/lista/uczestnikow", code=302)
    
@login_required
def costs():
    attendant = Attendant.query.filter(Attendant.email == session['email']).first()
    if request.method == 'GET':
        attendant = {
            "fname": attendant.fname,
            "lname": attendant.lname,
            "email": attendant.email,
            "academic_title":attendant.academic_title,
            "is_banquet":attendant.is_banquet,
            "is_tour":attendant.is_tour,
            "universities": attendant.universities,
            "lectures": attendant.lectures,
            "rents": attendant.rents,
            "costs": attendant.costs
        }
        
    return render_template('costs.html', attendant=attendant)