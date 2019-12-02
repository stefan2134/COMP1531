import csv

class Appointment ():

    def __init__ (self, patient, provider, healthcare_centre, datetime, patient_note=None, provider_comment=None, provider_medication=None, referral=None):
        self._patient = patient
        self._provider = provider
        self._healthcare_centre = healthcare_centre
        self._datetime = datetime
        self._patient_note = patient_note
        self._provider_comment = provider_comment
        self._provider_medication = provider_medication
        self._referral = referral

    @property
    def patient(self):
        return self._patient
        
    @patient.setter
    def patient(self, patient):
        self._patient = patient
        
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
    def datetime(self):
        return self._datetime

    @datetime.setter
    def datetime(self, datetime):
        self._datetime = datetime
        
    @property
    def patient_note(self):
        return self._patient_note

    @patient_note.setter
    def patient_note(self, patient_note):
        self._patient_note = patient_note
        
    @property
    def provider_comment(self):
        return self._provider_comment

    @provider_comment.setter
    def provider_comment(self, provider_comment):
        self._provider_comment = provider_comment
        
    @property
    def provider_medication(self):
        return self._provider_medication

    @provider_medication.setter
    def provider_medication(self, provider_medication):
        self._provider_medication = provider_medication
	
    @property
    def referral(self):
        return self._referral

    @referral.setter
    def referral(self, referral):
        self._referral = referral

    def update_details(self, comment, medication, referral=None):
        self._provider_medication = medication
        self._provider_comment = comment
        self.remove_data(1)
        self.append_data(1)

    def append_data(self, past):
        filename = 'data/current_appointment.csv'
        info = [self._patient.email_address, self._provider.email_address, self._healthcare_centre.name, self._datetime.month, self._datetime.day, self._datetime.hour, self._datetime.minute, self._patient_note]
        if past == 1:
            filename = 'data/past_appointment.csv'
            info += [self._provider_comment, self._provider_medication]
            if self._referral != None:
                info += [self._referral.id]
        with open(filename, 'a') as file:
            writer = csv.writer(file)
            writer.writerow(info)
        file.close()

    def remove_data(self, past):
        filename = 'data/current_appointment.csv'
        string = self._patient.email_address+","+self._provider.email_address+","+self._healthcare_centre.name+","+str(self._datetime.month)+","+str(self._datetime.day)+","+str(self._datetime.hour)+","+str(self._datetime.minute)+","+self._patient_note
        if past == 1:
            filename = 'data/past_appointment.csv'
        with open(filename, 'r+') as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                if string not in line:
                    file.write(line)
            file.truncate()
            file.close()
