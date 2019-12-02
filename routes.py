from server import app, system
from flask import request, render_template, redirect, url_for
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from lib.user import Patient, Provider
from lib.appointment import Appointment
from lib.system import *
import datetime, calendar, copy
from lib.referral import Referral

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/', methods=['POST', 'GET'])
def showHome():
    if current_user.is_authenticated:
        if current_user.is_specialist():
            return render_template('homepage.html', appointments=len(system.get_current_appointments(current_user)), referrals=len(system.get_referrals(current_user)))
        return render_template('homepage.html', appointments=len(system.get_current_appointments(current_user)))
    else:
        return render_template('homepage.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = system.login_user(email, password)
            login_user(user)
            return redirect(url_for("showHome"))
        except LoginError as le:
            return render_template('login_page.html', error=le.errors)
    return render_template('login_page.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("showHome") )

@login_manager.user_loader
def load_user(email):
    return system.get_user(email)

@app.route("/search", methods=['GET', 'POST'])
@login_required
def search_healthcare_service():
    if request.method == 'POST':
        form = request.form['form']
        try:
            # obtain filter method and type of healthcare service
            if form == 'filter':
                service = request.form['service']
                filter = request.form['filter']
                return render_template('search.html', service=service, filter=filter)

            # obtain input for search
            elif form == 'input':
                service = request.form['service']
                filter = request.form['filter']
                input = request.form['input']
                search_results = system.search_healthcare_service(service=service, filter=filter, input=input)
                return render_template('search.html', results=search_results, service=service)
        except SearchError as err:
            return render_template('search.html', service=None, error=err.message)
    else:
        return render_template('search.html', service=None)

@app.route('/booking', methods=['POST', 'GET'])
@login_required
def make_booking():
    form = request.form['form']
    provider = system.get_provider(request.form['email'])
    referral = -1
    if 'referral' in request.form:
        referral = request.form['referral']
    if form == 'book':
        if 'centre_name' in request.form:
            return render_template('booking.html', provider=provider, referral=referral, centre=request.form['centre_name'])
        else:
            return render_template('booking.html', provider=provider, referral=referral, centres=system.get_centres_of_provider(provider))
    elif form == 'centre':
        return render_template('booking.html', provider=provider, referral=request.form['referral'], centre=request.form['centre'])
    elif form == 'month':
        month = request.form['month']
        tmp, days = calendar.monthrange(2018, int(month))
        return render_template('booking.html', provider=provider, referral=request.form['referral'], centre=request.form['centre'], month=month, dates=range(1, days+1))
    elif form == 'date':
        month = request.form['month']
        date = request.form['date']
        dateObj = datetime.date(2018,int(month),int(date))
        times = provider.is_available(system.current_appointments(),int(month),int(date))
        tmp, days = calendar.monthrange(2018, int(month))
        if len(times) == 0:
            return render_template('booking.html', provider=provider, referral=request.form['referral'], centre=request.form['centre'], month=month, date=date, selected_date=dateObj, times=times, dates=range(1, days+1), message="No timeslots are available. Please try again at a later time.")
        return render_template('booking.html', provider=provider, referral=request.form['referral'], centre=request.form['centre'], month=month, date=date, selected_date=dateObj, times=times, dates=range(1, days+1))

@app.route('/confirm', methods=['POST', 'GET'])
@login_required
def confirm_booking():
    month = request.form['month']
    date = request.form['date']
    centre = request.form['centre']
    selected_time = request.form['time']
    referral = request.form['referral']
    hour, minute, tmp = request.form['time'].split(":")
    provider = system.get_provider(request.form['email'])
    centreObj = system.get_centre(centre)
    datetimeObj = datetime.datetime(2018,int(month),int(date),int(hour),int(minute))
    userObj = system.get_patient(current_user.email_address)
    note = None
    if 'note' in request.form:
        note = request.form['note']
    try:
        appointmentObj = system.add_appointment(userObj, provider, centreObj, datetimeObj, note, int(referral))
        return render_template('booking.html', appointmentObj=appointmentObj, confirm=True)
    except BookingError as be:
        dateObj = datetime.date(2018,int(month),int(date))
        tmp, days = calendar.monthrange(2018, int(month))
        times = provider.is_available(system.current_appointments(),month,date)
        tmp, days = calendar.monthrange(2018, int(month))
        dates = range(1, days+1)
        return render_template('booking.html', errors=be.errors, provider=provider, centre=centre, month=month, date=date, formatted_date=dateObj, times=times, dates=dates, referral = referral)

@app.route("/profile/centre/<name>", methods=['GET', 'POST'])
@login_required
def centre_profile(name):
    centre = system.get_centre(name)
    provider_list = system.get_providers_of_centre(centre)
    if "rating" in request.form:
        rating = request.form['rating']
        centre.add_rating(current_user, int(rating))
        return render_template('profile.html', service=centre, provider_list=provider_list, rating=rating, user = current_user)
    return render_template('profile.html', service=centre, provider_list=provider_list, user = current_user)

@app.route("/profile/provider/<email_address>", methods=['GET', 'POST'])
@login_required
def provider_profile(email_address):
    provider = system.get_provider(email_address)
    centre_list = system.get_centres_of_provider(provider)
    if "rating" in request.form:
        rating = request.form['rating']
        provider.add_rating(current_user, int(rating))
        return render_template('profile.html', service=provider, centre_list=centre_list, rating=rating, user=current_user)
    return render_template('profile.html', service=provider, centre_list=centre_list, user=current_user)

#patient patient
@app.route("/profile_page", methods=['GET', 'POST'])
@login_required
def profile_page():

    if request.method == "POST":
        return render_template('profile_page.html', update=True)
    return render_template('profile_page.html')


@app.route("/update_profile", methods=['GET', 'POST'])
@login_required
def update_profile():

    details = {}
    if request.method == "POST":

        details['name'] = request.form["name"]
        details['phone_number'] = request.form["phone_number"]
        current_user.update_details(details)

    return redirect(url_for("profile_page"))

@app.route("/history", methods=['GET', 'POST'])
@login_required
def view_own_history():
    past_results = system.get_past_appointments(current_user)
    current_results = system.get_current_appointments(current_user)
    return render_template('history.html', current_appointments=current_results, past_appointments=past_results)

@app.route("/appointment_details", methods=['GET', 'POST'])
@login_required
def appointment_details():
    provider = system.get_provider(request.form['provider'])
    appointment = system.get_appointment(provider, request.form['datetime'])
    return render_template('appointment_details.html', result=appointment)


@app.route("/patient_history", methods=['GET', 'POST'])
@login_required
def view_patient_history():
    patient_list = system.get_patient_list(current_user)
    if request.method == "POST":
        patient = system.get_patient(request.form['patient'])
        current_results = system.get_current_appointments(patient)
        past_results = system.get_past_appointments(patient)
        return render_template('patient_history.html', patient=patient, patient_list=patient_list, current_appointments=current_results, past_appointments=past_results)

    else:
        return render_template('patient_history.html', patient_list=patient_list)

@app.route("/consultation", methods=['GET', 'POST'])
@login_required
def document_consultation():
    form = request.form['form']
    provider = system.get_provider(request.form['provider'])
    datetime_str = request.form['datetime']
    appointment = system.get_appointment(provider, datetime_str)
    if form == 'edit':
        if provider.is_gp() and appointment.referral != None:
            return render_template('document_consultation.html', appointment=appointment, referral=appointment.referral, edit=True, refer=True)
        return render_template('document_consultation.html', appointment=appointment, edit=True)
    if form == 'save' or form == 'save_edit':
        comment = request.form['comment']
        medication = request.form['medication']
        if form == 'save':
            system.move_appointment(appointment)
            if provider.is_gp():
                if request.form['specialist'] != "":
                    specialist = system.get_provider(request.form['specialist'])
                    date = datetime.date(2018, appointment.datetime.month, appointment.datetime.day)
                    referral = Referral(appointment.patient, specialist, date, request.form['referral'], system.get_referral_id())
                    system.add_referral(referral)
                    appointment.update_details(comment, medication, referral)
                    return render_template('document_consultation.html', appointment=appointment, referral=referral, save=True, refer=True)
        appointment.update_details(comment, medication);
        return render_template('document_consultation.html', appointment=appointment, save=True)
    return render_template('document_consultation.html', appointment=appointment, specialists=system.specialists())

@app.route("/referral", methods=['GET'])
@login_required
def get_referrals():
    return render_template('referral.html', referrals=system.get_referrals(current_user))
