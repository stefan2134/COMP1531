from abc import ABC, abstractmethod
from flask_login import UserMixin #for login thing
from enum import Enum
from datetime import time
from lib.rating import Rating
import copy, random, csv
from lib.manager.rating_manager import RatingManager

class ProviderService(Enum):
    GP = "General Practitioner"
    PHARMACIST = "Pharmacist"
    PHYSIOTHERAPIST = "Physiotherapist"
    PATHOLOGIST = "Pathologist"
    SPECIALIST = "Specialist"

    def is_valid(service):
        for valid_service in ProviderService:
            if service.upper() == valid_service.name:
                return valid_service.value
        return 0

class HealthcareCentreCategory(Enum):
    MEDICALCENTRE = "Medical Centre"
    HOSPITAL = "Hospital"

    def is_valid(category):
        for valid_category in HealthcareCentreCategory:
            if category.upper() == valid_category.name:
                return valid_category.value
        return 0

class User(ABC, UserMixin):

    def __init__ (self, full_name, email_address, phone_number, password):
        self._full_name = full_name
        self._email_address = email_address
        self._phone_number = phone_number
        self._password = password

    @property
    def full_name(self):
        return self._full_name

    @full_name.setter
    def full_name(self, full_name):
        self._full_name = full_name

    @property
    def email_address(self):
        return self._email_address

    @email_address.setter
    def email_address(self, email_address):
        self._email_address = email_address

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, phone_number):
        self._phone_number = phone_number

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    def get_id(self):
        #unique id for each user
        return self.email_address

    def update_details(self, details):
        if details["name"] != "" :
            self._full_name = details["name"]
        if details["phone_number"] != "" :
            self._phone_number = details["phone_number"]
        self.remove_data()
        self.append_data()

    @abstractmethod
    def is_provider(self):
        pass

    @abstractmethod
    def is_specialist(self):
        pass

    @abstractmethod
    def get_history(self, appointments):
        pass

    @abstractmethod
    def append_data(self):
        pass

    @abstractmethod
    def remove_data(self):
        pass

class HealthcareService(ABC):
    def __init__ (self):
        self._rating_manager = RatingManager()

    @property
    def rating_manager(self):
        return self._rating_manager
        
    def ratings(self):
        return self.rating_manager.ratings
    
    def add_rating(self, patient, value): 
        return self.rating_manager.add_rating(self, patient, value)   
    
    def calculate_average_rating(self):
        return self.rating_manager.calculate_average_rating()

    @abstractmethod
    def is_provider(self):
        pass

    @abstractmethod
    def is_specialist(self):
        pass

    @abstractmethod
    def is_centre(self):
        pass

class Patient(User):
    def __init__ (self, full_name, email_address, password, phone_number, medicare_number):
        User.__init__(self, full_name, email_address, phone_number, password)
        self._medicare_number = medicare_number

    @property
    def medicare_number(self):
        return self._medicare_number

    @medicare_number.setter
    def medicare_number(self, medicare_number):
        self._medicare_number = medicare_number

    def is_provider(self):
        return False

    def is_specialist(self):
        return False

    def get_history(self, appointments):
        results = []
        for appointment in appointments:
            if appointment.patient == self:
                results.append(appointment)
        return results

    def append_data(self):
        with open('data/patient.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow([self._full_name, self._email_address, self._password, self._phone_number, self._medicare_number])
        file.close()

    def remove_data(self):
        with open('data/patient.csv', 'r+') as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                if self._email_address not in line:
                    file.write(line)
            file.truncate()
        file.close()

class Provider(User, HealthcareService):
    def __init__ (self, full_name, email_address, password, phone_number, service, provider_number):
        if ProviderService.is_valid(service) == 0:
            raise ValueError('Provider Service not valid')
        User.__init__(self, full_name, email_address, phone_number, password)
        HealthcareService.__init__(self)
        self._provider_number = provider_number
        self._service = ProviderService[service.upper()].value

    @property
    def provider_number(self):
        return self._provider_number

    @provider_number.setter
    def provider_number(self, provider_number):
        self._provider_number = provider_number

    @property
    def service(self):
        return self._service

    @service.setter
    def service(self, service):
        self._service = service

    def is_available(self, appointments, month, date):
        times = []
        minutes = [0, 30]
        for hour in range(9,17):
            for minute in minutes:
                times.append(time(hour,minute))
        for appointment in appointments:
            if appointment.datetime.month == month and appointment.datetime.day == date and appointment.provider == self:
                times.remove(time(appointment.datetime.hour,appointment.datetime.minute))
        return times
  
    def is_provider(self):
        return True

    def is_gp(self):
        if self._service == 'General Practitioner':
            return True
        return False

    def is_specialist(self):
        return False

    def is_centre(self):
        return False

    def get_history(self, appointments):
         results = []
         for appointment in appointments:
             if appointment.provider == self:
                 results.append(appointment)
         return results

    def append_data(self):
        with open('data/provider.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow([self._full_name, self._email_address, self._password, self._phone_number, ProviderService(self._service).name, self._provider_number])
        file.close()
        for r in self.ratings():
            r.append_data(self)

    def remove_data(self):
        with open('data/provider.csv', 'r+') as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                if self._email_address not in line:
                    file.write(line)
            file.truncate()
        file.close()

class Specialist(Provider):
    def __init__(self, full_name, email_address, password, phone_number, service, provider_number, expertise=None):
        Provider.__init__(self, full_name, email_address, password, phone_number, service, provider_number)
        self._expertise = expertise
        self._inbox = []
    
    @property
    def expertise(self):
        return self._expertise

    @property
    def inbox(self):
        return self._inbox

    @expertise.setter
    def expertise(self, expertise):
        self._expertise = expertise

    def is_specialist(self):
        return True

    def append_data(self):
        super().append_data()
        with open('data/specialist.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow([self._email_address, self._expertise])
        file.close()

class HealthcareCentre(HealthcareService):
    def __init__ (self, category, abn_number, name, phone_number, suburb):
        if HealthcareCentreCategory.is_valid(category) == 0:
            raise ValueError('Healthcare Centre type not valid')
        HealthcareService.__init__(self)
        self._name = name
        self._category = HealthcareCentreCategory[category.upper()].value
        self._abn_number = abn_number
        self._suburb = suburb
        self._phone_number = phone_number

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, password):
        self._category = category

    @property
    def abn_number(self):
        return self._abn_number

    @abn_number.setter
    def abn_number(self, abn_number):
        self._abn_number = abn_number

    @property
    def suburb(self):
        return self._suburb

    @suburb.setter
    def suburb(self, suburb):
        self._suburb = suburb

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, phone_number):
        self._phone_number = phone_number

    def is_provider(self):
        return False

    def is_specialist(self):
        return False

    def is_centre(self):
        return True

    def append_data(self):
        with open('data/health_centres.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow([HealthcareCentreCategory(self._category).name, self._abn_number, self._name, self._phone_number, self._suburb])
        file.close()
        for r in self.ratings():
            r.append_data(self)
