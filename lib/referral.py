import csv

class Referral():
    def __init__(self, patient, specialist, date, message, id, appointment=None):
        self._patient = patient
        self._specialist = specialist
        self._date = date
        self._message = message
        self._id = id
        self._appointment = None

    @property
    def patient(self):
        return self._patient

    @property
    def specialist(self):
        return self._specialist

    @property
    def date(self):
        return self._date

    @property
    def message(self):
        return self._message

    @property
    def id(self):
        return self._id

    @property
    def appointment(self):
        return self._appointment

    @appointment.setter
    def appointment(self, appointment):
        self._appointment = appointment

    def update_details(self, appointment):
        self._appointment = appointment
        self.remove_data()
        self.append_data()

    def append_data(self):
        info = [self._patient.email_address, self._specialist.email_address, self._date.month, self._date.day, self._message, self._id]
        if self._appointment != None:
            info += [self._appointment.provider.email_address, self._appointment.datetime.strftime("%d-%m-%Y %H:%M")]
        with open ('data/referral.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(info)
        file.close()

    def remove_data(self):
        string = self._patient.email_address+","+self._specialist.email_address+","+str(self._date.month)+","+str(self._date.day)+","+self._message+","+str(self._id)
        with open('data/referral.csv', 'r+') as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                if string not in line:
                    file.write(line)
            file.truncate()
            file.close()
