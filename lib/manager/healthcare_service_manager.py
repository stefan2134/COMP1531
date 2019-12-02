from lib.error import *
from lib.appointment import Appointment
from lib.employment import Employment
from lib.referral import Referral
from abc import ABC, abstractmethod
from lib.user import *
import copy, datetime, csv, os

class HealthcareServiceManager():
    def __init__(self, provider_manager):
        self._centre_manager = HealthcareCentreManager();
        self._provider_manager = provider_manager

    @property
    def centre_manager(self):
        return self._centre_manager

    @property
    def provider_manager(self):
        return self._provider_manager

    def search_service(self, service, filter, input):
        search_results = []
        if service == 'centre':
            search_results = self._centre_manager.search_centre(filter, input)
        elif service == 'provider':
            search_results = self._provider_manager.search_provider(filter,input)
        else:
            raise SearchError("Invalid healthcare service")
        return search_results

    def save_data(self):
        open('data/health_centres.csv', 'w').close()
        for c in self._centre_manager.centres:
            c.append_data()

    def load_data(self, system):
        # reads centre data in order: category, abn number, name, phone number, suburb
        with open('data/health_centres.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                self._centre_manager.add_centre(HealthcareCentre(row[0], row[1], row[2], row[3], row[4]))

        try:
            with open('data/rating.csv') as file:
                reader = csv.reader(file)
                for row in reader:
                    service = system.get_centre(row[0])
                    patient = system.get_patient(row[1])
                    if service != None and patient != None:
                        service.add_rating(patient, row[2])
        except Exception as err:
            print(err.args)


class HealthcareCentreManager():

    def __init__(self):
        self._centres = []

    @property
    def centres(self):
        return self._centres

    def add_centre(self, centre):
        return self._centres.append(centre)

    def get_centre(self, name):
        for centre in self._centres:
            if centre.name == name:
                return centre
        return None

    def search_centre(self, filter, input):
        search_results = []
        if filter == 'name':
            for centre in self._centres:
                if input.lower() in centre.name.lower():
                    search_results.append(centre)
        elif filter == 'suburb':
            for centre in self._centres:
                if input.lower() in centre.suburb.lower():
                    search_results.append(centre)
        else:
            raise SearchError("Invalid filter method")
        return search_results

