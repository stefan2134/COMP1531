from lib.error import *
from lib.appointment import Appointment
from lib.employment import Employment
from lib.referral import Referral
from abc import ABC, abstractmethod
from lib.user import *
import copy, datetime, csv, os

class EmploymentManager():

    def __init__(self):
        self._employments = []

    @property
    def employments(self):
        return self._employments

    def add_employment(self, employment):
        self._employments.append(employment)
        
    def get_provider_list(self, centre):
        provider_list = []
        for employment in self._employments:
            if employment.healthcare_centre == centre:
                provider_list.append(employment)
        print(provider_list)
        return provider_list

    def get_employment_provider_list(self, centre):
        provider_list = []
        for employment in self._employments:
            if employment.healthcare_centre == centre:
                provider_list.append(employment)
        print(provider_list)
        return provider_list

    def get_centre_list(self, provider):
        centre_list = []
        for employment in self._employments:
            if employment.provider == provider:
                centre_list.append(employment)
        return centre_list

    def save_data(self):
        open('data/employment.csv', 'w').close()
        for e in self._employments:
            e.append_data()

    def load_data(self, system):
        try:
            # read employment data in order: provider, centre
            with open('data/employment.csv') as file:
                reader = csv.reader(file)
                for row in reader:
                    provider = system.get_provider(row[0])
                    centre = system.get_centre(row[1])
                    if centre != None and provider != None:
                        system.add_employment(Employment(provider, centre, datetime.time(9), datetime.time(17)))
        except Exception as err:
            print(err.args)

