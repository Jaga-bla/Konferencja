from src.models.models import Attendant, University
import re


def attendant_form(form, attendant=None)->Attendant:
    if attendant is None:
        fname = form['fname']
        lname = form['lname']
        academic_title = form['degree']
        if academic_title == "":
            academic_title=None
        is_banquet = form.get('is_banquet',0)
        is_tour = form.get('is_tour',0)
        email = form.get('email')
        
        if email and not is_valid_email(email):
            raise ValueError("Invalid email address")
        
        is_banquet=False if int(is_banquet)==0 else True
        is_tour=False if int(is_tour)==0 else True
        
        attendant = Attendant(fname, lname, email,  academic_title, is_banquet=is_banquet, is_tour=is_tour)
        return attendant
    else:
        attendant.fname = form['fname']
        attendant.lname = form['lname']
        attendant.academic_title = form['degree']
        is_banquet = form.get('is_banquet',0)
        is_tour = form.get('is_tour',0)
        attendant.email = form.get('email')
        attendant.is_banquet=False if int(is_banquet)==0 else True
        attendant.is_tour=False if int(is_tour)==0 else True
        return attendant

def univeristy_form(form, university=None)->University:
    if university==None:
        name = form['name']
        street = form['street']
        city = form['city']
        code = form['code']
        contry = form['country'] 
        nip = form.get('nip')
        university = University(name, street, city, code, contry, nip)
    else:
        university.name = form['name']
        university.street = form['street']
        university.city = form['city']
        university.code = form['code']
        university.contry = form['country'] 
        university.nip = form.get('nip')
    return university

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None