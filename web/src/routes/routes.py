from datetime import datetime
from flask import Blueprint

from src import app

from src.controllers.lectures_views import lectures, add_lecture, edit_lecture
from src.controllers.attendants_views import registration, edit_attendant, costs, login, logout
from src.controllers.rooms_views import rooms
from src.controllers.university_views import add_university, edit_university
from src.controllers.admin_views import attendants_list, analytics


konf = Blueprint('konf', __name__)

konf.route('/prezentacje', methods=['GET'])(lectures)
konf.route('/dodaj/prezentacje', methods=['GET', 'POST'])(add_lecture)
konf.route('/edytuj/prezentacje/<lecture_id>', methods=['GET', 'POST', 'DELETE'])(edit_lecture)

konf.route('/lista/uczestnikow', methods=['GET','POST'])(attendants_list)
konf.route('/statystyka', methods = ['GET', 'POST'])(analytics)

konf.route('/rejestracja', methods = ['GET','POST'])(registration)
konf.route('/login', methods=['GET', 'POST'])(login)
konf.route('/logout', methods=['GET', 'POST'])(logout)
konf.route('/edytuj/uczestnika/<att_id>', methods = ['GET','POST'])(edit_attendant)
konf.route('/koszty', methods = ['GET'])(costs)

konf.route('/hotel', methods=['GET','POST'])(rooms)

konf.route('/dodaj/uniwersytet', methods=['GET', 'POST'])(add_university)
konf.route('/edytuj/uniwerytet/<univ_id>', methods = ['GET','POST'])(edit_university)

app.register_blueprint(konf, url_prefix='/')