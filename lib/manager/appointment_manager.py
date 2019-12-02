from lib.error import *
from lib.appointment import Appointment
from lib.employment import Employment
from lib.referral import Referral
from abc import ABC, abstractmethod
from lib.user import *
import copy, datetime, csv, os

class AppointmentManager():

    def __init__(self):
        self._current_appointments = []
        self._past_appointments = []

    @property
    def current_appointments(self):
        return self._current_appointments

    @property
    def past_appointments(self):
        return self._past_appointments

    def add_current_appointment(self, appointment):
        self._current_appointments.append(appointment)
        appointment.append_data(0)

    def add_past_appointment(self, appointment):
        self._past_appointments.append(appointment)
        appointment.append_data(1)

    def remove_current_appointment(self, appointment):
        self._current_appointments.remove(appointment)
        appointment.remove_data(0)

    def add_appointment(self, userObj, providerObj, centreObj, datetimeObj, note, referral, centre_list):
        errors = {}
        if userObj == None or userObj.is_provider() or userObj.is_specialist():
            errors['user'] = "Please login as a patient"
        if providerObj is None or providerObj.is_provider == False:
            errors['Unknown provider or specialist'] = "Error: cannot book an appointment with the selected provider"
        elif providerObj not in [x.provider for x in centre_list]:
            print(providerObj.full_name+" "+centreObj.name)
            print(providerObj)
            errors['Provider/Centre Relation'] = "Provider does not work at this centre"
        if centreObj is None:
            errors['centre'] = "Please select a centre"
        if datetimeObj is None:
            errors['time'] = "Please select a time slot"
        else:
            time = datetime.time(datetimeObj.hour, datetimeObj.minute)
            times = providerObj.is_available(self.current_appointments, datetimeObj.month, datetimeObj.day)
            if time not in times:
                errors['time'] = "The provider is not available at this time, please select a different time"
            for appointment in self.current_appointments + self.past_appointments:
                if datetimeObj == appointment.datetime and userObj == appointment.patient:
                    errors['double book warning'] = "You already have an appointment at this time"
                    
        if providerObj.is_specialist():
            if referral == 0:
                errors['No referral'] = "You need a referral to book with a specialist"
                  
        if errors:
          raise BookingError(errors)
        
        userObj = copy.copy(userObj)
        appointmentObj = Appointment(userObj, providerObj, centreObj, datetimeObj, patient_note=note)
        if referral != None:
            referral.appointment = appointmentObj
        self.add_current_appointment(appointmentObj)
        return appointmentObj

    def move_appointment(self, appointment):
        self.remove_current_appointment(appointment)
        self.add_past_appointment(appointment)

    def get_appointment(self, provider, datetime):
        for appointment in self._current_appointments + self._past_appointments:
            if appointment.provider == provider and appointment.datetime.strftime("%d-%m-%Y %H:%M") == datetime:
                return appointment
        return None

    def get_patient_list(self, provider):
        results = []
        for appointment in self._current_appointments + self._past_appointments:
            if appointment.provider == provider and appointment.patient not in results:
                results.append(appointment.patient)
        return results

    def save_data(self):
        open('data/current_appointment.csv', 'w').close()
        open('data/past_appointment.csv', 'w').close()
        for a in self._current_appointments:
            a.append_data(0)
        for a in self._past_appointments:
            a.append_data(1)

    def load_data(self, system):
        #if os.path.exists('data/current_appointment.csv'):
        try:
            with open('data/current_appointment.csv') as file:
                reader = csv.reader(file)
                for row in reader:
                    patient = system.get_patient(row[0])
                    provider = system.get_provider(row[1])
                    centre = system.get_centre(row[2])
                    datetimeObj = datetime.datetime(2018, int(row[3]), int(row[4]), int(row[5]), int(row[6]))
                    patient_note = None
                    if len(row) > 7:
                        patient_note = row[7]                    
                    if patient != None and provider != None and centre != None:
                        self._current_appointments.append(Appointment(patient, provider, centre, datetimeObj, patient_note))
        except Exception as err:
            print(err.args)

        #if os.path.exists('data/past_appointment.csv'):
        try:
            with open('data/past_appointment.csv') as file:
                reader = csv.reader(file)
                for row in reader:
                    patient = system.get_patient(row[0])
                    provider = system.get_provider(row[1])
                    centre = system.get_centre(row[2])
                    datetimeObj = datetime.datetime(2018, int(row[3]), int(row[4]), int(row[5]), int(row[6]))
                    patient_note = None
                    comment = None
                    medication = None
                    referral = None
                    print(patient.full_name+" "+provider.full_name+" "+centre.name+" "+datetimeObj.strftime("%d-%m-%Y %H:%M"))
                    if len(row) > 10:
                        referral = system.get_referral(row[10])
                    if len(row) > 9:
                        medication = row[9]
                    if len(row) > 8:
                        comment = row[8]
                    if len(row) > 7:
                        patient_note = row[7]                    
                    if patient != None and provider != None and centre != None:
                        self._past_appointments.append(Appointment(patient, provider, centre, datetimeObj, patient_note, comment, medication, referral))
        except Exception as err:
            print(err.args)

