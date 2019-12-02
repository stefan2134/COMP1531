from lib.error import *
from lib.appointment import Appointment
from lib.employment import Employment
from lib.referral import Referral
from abc import ABC, abstractmethod
from lib.user import *
from lib.manager.user_manager import *
from lib.manager.healthcare_service_manager import *
from lib.manager.employment_manager import *
from lib.manager.appointment_manager import *
from lib.manager.referral_manager import *
import copy, datetime, csv, os

class HamsSystem():

    def __init__(self):
        self._user_manager = UserManager()
        self._healthcare_service_manager = HealthcareServiceManager(self._user_manager.provider_manager)
        self._appointment_manager = AppointmentManager()
        self._employment_manager = EmploymentManager()
        self._referral_manager = ReferralManager()

    @property
    def user_manager(self):
        return self._user_manager

    @property
    def healthcare_service_manager(self):
        return self._healthcare_service_manager

    @property
    def appointment_manager(self):
        return self._appointment_manager

    @property
    def employment_manager(self):
        return self._employment_manager

    @property
    def referral_manager(self):
        return self._referral_manager

    def patients(self):
        return self._user_manager.patient_manager.patients

    def providers(self):
        return self._user_manager.provider_manager.providers

    def specialists(self):
        return self._user_manager.provider_manager.specialists

    def current_appointments(self):
        return self._appointment_manager.current_appointments

    def get_id(self):
        return self._user_manager.get_id();

    def get_referral_id(self):
        return self._referral_manager.get_id()

    def get_user(self, email_address):
        return self._user_manager.get_user(email_address)

    def get_patient(self, email_address):
        return self._user_manager.patient_manager.get_patient(email_address)

    def get_provider(self, email_address):
        return self._user_manager.provider_manager.get_provider(email_address)

    def get_centre(self, name):
        return self._healthcare_service_manager.centre_manager.get_centre(name)

    def get_appointment(self, provider, datetime):
        return self._appointment_manager.get_appointment(provider, datetime)

    def get_referral(self, id):
        return self._referral_manager.get_referral(id)

    def get_patient_list(self, provider):
        return self._appointment_manager.get_patient_list(provider)

    def get_referrals(self, user):
        return self._referral_manager.get_referrals(user)

    def get_centres_of_provider(self, provider):
        return self._employment_manager.get_centre_list(provider)

    def get_providers_of_centre(self, centre):
        return self._employment_manager.get_employment_provider_list(centre)

    def search_healthcare_service(self, service, filter, input):
        return self._healthcare_service_manager.search_service(service, filter, input)

    def add_patient(self, patient):
        self._user_manager.patient_manager.add_patient(patient)

    def add_provider(self, provider):
        self._user_manager.provider_manager.add_provider(provider)

    def add_centre(self, centre):
        self._healthcare_service_manager.centre_manager.add_centre(centre)

    def add_employment(self, employment):
        self._employment_manager.add_employment(employment)

    def add_current_appointment(self, appointment):
        self._appointment_manager.add_current_appointment(appointment)

    def add_past_appointment(self, appointment):
        self._appointment_manager.add_past_appointment(appointment)

    def add_referral(self, referral):
        self._referral_manager.add_referral(referral)

    def move_appointment(self, appointment):
        self._referral_manager.remove_referral(appointment)
        self._appointment_manager.move_appointment(appointment)

    def document_consultation(self, appointment, comment, medication, referral=None):
        self._appointment_manager.document_consultation(appointment, comment, medication, referral)

    def get_current_appointments(self, user):
        return user.get_history(self._appointment_manager.current_appointments)

    def get_past_appointments(self, user):
        return user.get_history(self._appointment_manager.past_appointments)

    def add_appointment(self, userObj, providerObj, centreObj, datetimeObj, note, referral_id):
        referral = self._referral_manager.get_referral(referral_id)
        if centreObj is not None:
        	centre_provider_list = self._employment_manager.get_provider_list(centreObj)
        else:
        	centre_provider_list = []	
        appointmentObj = self._appointment_manager.add_appointment(userObj, providerObj, centreObj, datetimeObj, note, referral, centre_provider_list)
        return appointmentObj

    def login_user(self, email_address, password):
        return self._user_manager.login_user(email_address, password)

    def save_data(self):
        self._user_manager.save_data()
        self._healthcare_service_manager.save_data()
        self._employment_manager.save_data()
        self._referral_manager.save_data()
        self._appointment_manager.save_data()

    def load_data(self):
        self._user_manager.load_data(self)
        self._healthcare_service_manager.load_data(self)
        self._employment_manager.load_data(self)
        self._referral_manager.load_data(self)
        self._appointment_manager.load_data(self)
