from lib.error import *
from lib.appointment import Appointment
from lib.employment import Employment
from lib.referral import Referral
from abc import ABC, abstractmethod
from lib.user import *
import copy, datetime, csv, os

class ReferralManager():
    def __init__(self):
        self._referrals = []
        self._id = -1

    @property
    def referrals(self):
        return self._referrals

    @property
    def id(self):
        return self._id

    def get_id(self):
        self._id += 1
        return self._id

    def get_referral(self, id):
        if id > 0:
            for referral in self._referrals:
                if referral.id == id:
                    return referral
        return None

    def add_referral(self, referral):
        self._referrals.append(referral)
        referral.append_data()

    def remove_referral(self, appointment):
        for referral in self._referrals:
            if referral.appointment == appointment:
                self._referrals.remove(referral)
        self.save_data()

    def get_referrals(self, user):
        referrals = []
        for referral in self._referrals:
            if referral.specialist == user or referral.patient == user:
                referrals.append(referral)
        return referrals

    def save_data(self):
        open('data/referral.csv', 'w').close()
        for r in self._referrals:
            r.append_data()

    def load_data(self, system):
        try:
            with open('data/referral.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    patient = system.get_patient(row[0])
                    specialist = system.get_provider(row[1])
                    datetimeObj = datetime.datetime(2018, int(row[2]), int(row[3]))
                    message = row[4]
                    id = row[5]
                    appointment = None
                    if len(row) > 6:
                        appointment_provider = system.get_provider(row[6])
                        appointment_datetime = row[7]
                        if appointment_provider != None:
                            appointment = system.get_appointment(appointment_provider, appointment_datetime)
                    if patient != None and specialist != None:
                        self._referrals.append(Referral(patient, specialist, datetimeObj, message, id, appointment))
        except Exception as err:
            print(err.args)
