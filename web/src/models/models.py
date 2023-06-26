from datetime import date

from src import db

att_univ = db.Table('att_univ',
    db.Column('att_id', db.Integer, db.ForeignKey('attendants.att_id'), primary_key=True),
    db.Column('univ_id', db.Integer, db.ForeignKey('universities.univ_id'), primary_key=True)
)   

class Attendant(db.Model):
    __tablename__ = "attendants"
    att_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(128), unique=False, nullable=False)
    lname = db.Column(db.String(128), unique=False, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    academic_title = db.Column(db.String(128), unique=False, nullable=True)
    is_banquet = db.Column(db.Boolean(), default=False, nullable=False)
    is_tour = db.Column(db.Boolean(), default=False, nullable=False)
    costs = db.Column(db.Float, default=0, nullable=False)
    universities = db.relationship('University', secondary = att_univ, backref = 'attendants')
    password = db.Column(db.String(128))
    
    rents_rs = db.relationship("Rent", backref="attendant", cascade="all, delete")
    lectures_rs = db.relationship("Lecture", backref="attendant", cascade="all, delete")
    
    def __init__(self, fname, lname, email, academic_title, is_tour = False, is_banquet=False):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.academic_title = academic_title
        self.is_tour = is_tour
        self.is_banquet = is_banquet
        
    def __repr__(self):
        return f"{self.fname} {self.lname}"
    
    @property
    def rents(self):
        return Rent.query.filter(Rent.att_id == self.att_id)
    
    @property
    def lectures(self):
        return Lecture.query.filter(Lecture.att_id == self.att_id)
    
class University(db.Model):
    __tablename__ = "universities"
    univ_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=False, nullable=False)
    street = db.Column(db.String(128), unique=False, nullable=False)
    city = db.Column(db.String(128), unique=False, nullable=False)
    code = db.Column(db.String(128), unique=False, nullable=False)
    country = db.Column(db.String(128), unique=False, nullable=False)
    NIP = db.Column(db.BIGINT)
    
    def __init__(self, name, street, city, code, country, NIP):
        self.name = name
        self.street = street
        self.city = city
        self.code = code
        self.country = country
        self.NIP = NIP
    
    def __repr__(self):
        return self.name

class Lecture(db.Model):
    __tablename__ = "lectures"
    lecture_id = db.Column(db.Integer, primary_key=True)
    att_id = db.Column(db.Integer, db.ForeignKey("attendants.att_id"), nullable = False)
    name = db.Column(db.String(128), unique=False, nullable=False)
    date = db.Column(db.DateTime, unique = True)
    
    def __init__(self, att_id, name, date):
        self.att_id = att_id
        self.name = name
        self.date = date
        
    def __repr__(self):
        return self.name
    
    @property
    def attendant(self):
        att =  Attendant.query.get(self.att_id)
        return att
    
    
class Room(db.Model):
    __tablename__ = "rooms"
    room_number = db.Column(db.Integer, primary_key=True)
    att_quantity = db.Column(db.Integer, unique=False, nullable=False)
    
    def __init__(self, room_number, att_quantity):
        self.room_number = room_number
        self.att_quantity = att_quantity
            
    def free(self, day):
        date_ = date(2023,6,day)
        rent = Rent.query.filter_by(date =date_).filter(Rent.room_number==self.room_number).first()
        if rent:
            return False
        else:
            return True
      
class Rent(db.Model):
    __tablename__ = "rents"
    rent_id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.Integer, db.ForeignKey("rooms.room_number"))
    att_id = db.Column(db.Integer, db.ForeignKey("attendants.att_id"))
    date = db.Column(db.Date)

    
    def __init__(self, room_number, att_id, date):
        self.room_number = room_number
        self.att_id = att_id
        self.date = date
        
    def __repr__(self):
        return f"Pokój nr {self.room_number} dnia {self.date}"