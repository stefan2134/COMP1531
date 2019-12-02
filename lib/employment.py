import csv

class Employment():

    def __init__ (self, provider, healthcare_centre, start_time, end_time):
        self._provider = provider
        self._healthcare_centre = healthcare_centre
        self._start_time = start_time
        self._end_time = end_time

    @property
    def provider(self):
        return self._provider

    @provider.setter
    def provider(self, provider):
        self._provider = provider

    @property
    def healthcare_centre(self):
        return self._healthcare_centre

    @healthcare_centre.setter
    def healthcare_centre(self, healthcare_centre):
        self._healthcare_centre = healthcare_centre

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        self._start_time = start_time

    @property
    def end_time(self):
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        self._end_time = end_time

    def append_data(self):
        with open('data/employment.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow([self._provider.email_address, self._healthcare_centre.name])
        file.close()
