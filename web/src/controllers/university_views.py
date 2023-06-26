from flask import render_template, request, redirect

from src import db
from src.models.models import University
from src.utils.forms import univeristy_form
from src.utils.decorators import login_required


def add_university():
    if request.method == 'POST':
        university = univeristy_form(request.form)
        
        db.session.add(university)
        db.session.commit()
        
        return redirect("/rejestracja", code=302)
    return render_template('university_form.html')


@login_required
def edit_university(univ_id):
    university = University.query.get_or_404(univ_id)

    if request.method == 'GET':
        university = {
            "univ_id" : university.univ_id,
            "name": university.name,
            "street": university.street,
            "city": university.city,
            "code": university.code,
            "country": university.country,
            "nip": university.NIP
        }
        return render_template('university_update.html', university=university)

    elif request.method == 'POST':
        university = univeristy_form(request.form, university)
        db.session.commit()
        
        return redirect("/prezentacje", code=302)