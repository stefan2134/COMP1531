import csv

class Rating():

    def __init__(self, patient, value):
        self._patient = patient
        self._value = value

    @property
    def patient(self):
	    return self._patient

    @patient.setter
    def patient(self, patient):
        self._patient = patient

    @property
    def value(self):
        return self._value

    @value.setter
    def end_time(self, value):
        self._value = value

    def append_data(self, service):
        with open('data/rating.csv', 'a') as file:
            writer = csv.writer(file)
            if service.is_provider():
                writer.writerow([service.email_address, self._patient.email_address, self._value])
            else:
                writer.writerow([service.name, self._patient.email_address, self._value])
        file.close()

    def remove_data(self, service):
        if service.is_provider():
            string = service.email_address+","+self._patient.email_address
        else:
            string = service.name+","+self._patient.email_address
        with open('data/rating.csv', 'r+') as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                if string not in line:
                    file.write(line)
                    print("this is fine: ")
                    print(">>>"+ line)
                    print(">>>"+ string)
            file.truncate()
        file.close()
