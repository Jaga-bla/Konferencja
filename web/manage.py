from datetime import datetime

from flask.cli import FlaskGroup

from src import app, db
from src.models.models import Room, Attendant, University, Lecture
from src.db.functions_triggers import FUNCTION_SET_COSTS, TRIGGERS_AFTER_INSERT_RENTS_ATTENDANTS

cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.execute(FUNCTION_SET_COSTS.execution_options(autocommit=True))
    db.session.execute(TRIGGERS_AFTER_INSERT_RENTS_ATTENDANTS.execution_options(autocommit=True))
    populate_db()

    
    
def populate_db():
    for number in range(101, 120, 2):
        room = Room(number, 1)
        db.session.add(room)
    for number in range(100, 120, 2):
        room = Room(number, 2)
        db.session.add(room)

    attendant1 = Attendant("Jacek", "Kowalski", "jacekkowalski@gmail.com", "Magister", True, True)
    attendant2 = Attendant("Anna", "Nowak", "annanowak@gmail.com", "Doktor", False, True)
    attendant3 = Attendant("Jan", "Nowicki", "jannowicki@gmail.com", "Inżynier", True, False)
    attendant4 = Attendant("Katarzyna", "Wójcik", "katarzynawojcik@gmail.com", "Licencjat", False, False)
    attendant5 = Attendant("Piotr", "Kowalczyk", "piotrkowalczyk@gmail.com", "Magister", True, True)
    university1 = University("Uniwersytet Kazimierza Wielkiego", "Żmudzka 45", "Bydgoszcz", "86-200", "Polska", 123123421)
    university2 = University("Uniwersytet Warszawski", "Krakowskie Przedmieście 26/28", "Warszawa", "00-927", "Polska", 987654321)
    university3 = University("Uniwersytet Jagielloński", "Golebia 24", "Kraków", "31-007", "Polska", 555555555)
    university4 = University("Politechnika Wrocławska", "Wybrzeże Wyspiańskiego 27", "Wrocław", "50-370", "Polska", 222222222)
    university5 = University("Uniwersytet im. Adama Mickiewicza", "Umultowska 89", "Poznań", "61-614", "Polska", 777777777)

    attendant1.universities.append(university1)
    attendant2.universities.append(university2)
    attendant3.universities.append(university3)
    attendant4.universities.append(university4)
    attendant5.universities.append(university5)
    
    db.session.add(attendant1)
    db.session.add(attendant2)
    db.session.add(attendant3)
    db.session.add(attendant4)
    db.session.add(attendant5)
    db.session.add(university1)
    db.session.add(university2)
    db.session.add(university3)
    db.session.add(university4)
    db.session.add(university5)
    db.session.commit()
    
    lecture1 = Lecture(attendant1.att_id, 'Fizyka Kwandowa', datetime(2023,6,26,11))
    lecture2 = Lecture(attendant1.att_id, 'Czarne dziury', datetime(2023,6,26,14))
    lecture3 = Lecture(attendant2.att_id, 'Teoria względności', datetime(2023,6,27,11))
    lecture4 = Lecture(attendant1.att_id, 'Energia odnawialna', datetime(2023,6,30,10))
    lecture5 = Lecture(attendant4.att_id, 'Fizyka w mechanice', datetime(2023,6,28,9))
    db.session.add(lecture1)
    db.session.add(lecture5)
    db.session.add(lecture4)
    db.session.add(lecture3)
    db.session.add(lecture2)

    db.session.commit()

if __name__ == "__main__":
    cli()
