from lib.error import *
from lib.user import *
import datetime, csv

class UserManager():

    def __init__(self):
        self._patient_manager = PatientManager()
        self._provider_manager = ProviderManager()
        self._id = -1;

    @property
    def patient_manager(self):
        return self._patient_manager

    @property
    def provider_manager(self):
        return self._provider_manager

    def get_id(self):
        self._id += 1
        return self._id

    def get_user(self, email_address):
        for user in self._patient_manager.patients + self._provider_manager.providers:
            if user.email_address == email_address:
                return user
        return None

    def login_user(self, email, password):
        errors = {}
        if email == "":
            errors['email'] = "Email is empty"
            if password == "":
                errors['password'] = "Password is empty"
            raise LoginError(errors)
        user = self.get_user(email)
        if user is None:
            errors['email'] = "Account not found"
            raise LoginError(errors)
        if user.password != password:
                errors['password'] = "Invalid username/password combination"
                raise LoginError(errors)
        return user

    def save_data(self):
        open('data/patient.csv', 'w').close()
        open('data/provider.csv', 'w').close()
        open('data/specialist.csv', 'w').close()
        open('data/rating.csv', 'w').close()
        for p in self._patient_manager.patients + self._provider_manager.providers:
            p.append_data()

    def load_data(self, system):
        # reads patient data in order: name, email, password, phone number, [medicare number]
        with open('data/patient.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) < 5:
                    id = self.get_id()
                else:
                    id = row[4]
                self._patient_manager.add_patient(Patient(row[0], row[1], row[2], row[3], id))

        # reads provider data in order: name, email, password, phone number, service, id
        with open('data/provider.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) < 6:
                    id = self.get_id()
                else:
                    id = row[5]
                if row[4].upper() == 'SPECIALIST':
                    self._provider_manager.add_provider(Specialist(row[0], row[1], row[2], row[3], row[4], id))
                else:
                    self._provider_manager.add_provider(Provider(row[0], row[1], row[2], row[3], row[4], id))

        with open('data/specialist.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                specialist = system.get_provider(row[0])
                if specialist != None:
                    specialist.expertise = row[1]

        try:
            with open('data/rating.csv') as file:
                reader = csv.reader(file)
                for row in reader:
                    service = system.get_provider(row[0])
                    patient = system.get_patient(row[1])
                    if service != None and patient != None:
                        service.ratings.append(Rating(patient, int(row[2])))

        except Exception as err:
            print(err.args)

class PatientManager():
    def __init__(self):
        self._patients = []

    @property
    def patients(self):
        return self._patients

    def add_patient(self, patient):
        self._patients.append(patient)

    def get_patient(self, email_address):
        for patient in self._patients:
            if patient.email_address == email_address:
                return patient
        return None

class ProviderManager():
    def __init__(self):
        self._providers = []
        self._specialists = []

    @property
    def providers(self):
        return self._providers

    @property
    def specialists(self):
        return self._specialists

    def add_provider(self, provider):
        self._providers.append(provider)
        if provider.is_specialist():
            self._specialists.append(provider)

    def get_provider(self, email_address):
        for provider in self._providers:
            if provider.email_address == email_address:
                return provider
        return None

    def search_provider(self, filter, input):
        search_results = []
        if filter == 'name':
            for provider in self._providers:
                if input.lower() in provider.full_name.lower():
                    search_results.append(provider)
        elif filter == 'service':
            for provider in self._providers:
                if input == provider.service:
                    search_results.append(provider)
        else:
            raise SearchError("Invalid filter method")
        return search_results
