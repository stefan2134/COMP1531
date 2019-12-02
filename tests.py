import pytest
from server import system
import datetime
from lib.system import *
# create a dummysystemclass
# create a dummy booking
# wrong email
# wrong centre Name
# wrong date
# note without note
#  (i) making a successful appointment and getting a confirmation of the appointment 
#  (ii)booking an appointment in the past
#  (iii) book multiple appointments in the same day/time-slot

#try and except
class TestBookAppointment(object):
    def setup_method(self):
        self.system = system 

    def test_successful_appointment_1(self):
        print ("test_successful_booking_appointment_1")

        providerObj = system.get_provider("toby@gmail.com")
        assert(providerObj.is_provider() == True)

        centreObj = system.get_centre("Sydney Children Hospital")
        assert(centreObj.is_centre() == True)

        userObj = system.get_patient("jack@gmail.com")
        assert(userObj.is_provider() == False)

        datetimeObj = datetime.datetime(2018,1,1,10,30)
        note = "I'm very sick, please help me doctor!"
        referral_id = 0 

        apmt = system.add_current_appointment(userObj, providerObj, centreObj, datetimeObj, note, referral_id)

        assert(apmt.patient.full_name == userObj.full_name)
        assert(apmt.provider == providerObj)
        assert(apmt.healthcare_centre == centreObj)
        assert(apmt.datetime == datetimeObj)
        assert(apmt.patient_note == note)
        apmt.patient_note = None
        assert(apmt.patient_note == None)

    def test_successful_appointment_2(self):
        print ("test_successful_booking_appointment_2")

        providerObj = system.get_provider("gary@gmail.com")
        assert(providerObj.is_provider() == True)

        centreObj = system.get_centre("USYD Health Service")
        assert(centreObj.is_centre() == True)

        userObj = system.get_patient("isaac@gmail.com")
        assert(userObj.is_provider() == False)

        datetimeObj = datetime.datetime(2018,1,1,10,30)
        note = "I'm dying, please help me doctor!"
        referral_id = 0 

        apmt = system.add_current_appointment(userObj, providerObj, centreObj, datetimeObj, note, referral_id)
        assert(apmt.patient.full_name == userObj.full_name)
        assert(apmt.provider == providerObj)
        assert(apmt.healthcare_centre == centreObj)
        assert(apmt.datetime == datetimeObj)
        assert(apmt.patient_note == note)
        apmt.patient_note = None
        assert(apmt.patient_note == None)

    def test_booking_same_appointment(self):
        print ("test_booking_same_appointment")
        #add a new appointment with same detail from above 
        providerObj = system.get_provider("gary@gmail.com")
        assert(providerObj.is_provider() == True)

        centreObj = system.get_centre("USYD Health Service")
        assert(centreObj.is_centre() == True)

        userObj = system.get_patient("isaac@gmail.com")
        assert(userObj.is_provider() == False)

        datetimeObj = datetime.datetime(2018,1,1,10,30)
        note = "I'm dying, please help me doctor!"
        referral_id = 0 

        try:
            apmt = system.add_current_appointment(userObj, providerObj, centreObj, datetimeObj, note, referral_id)
        except BookingError as be:
            print(be.msg)
            assert(be.msg =="Booking error occured with fields: double book warning")
            assert(True)
        else:
            assert(False)
        pass

    def test_booking_as_provider(self):

        print ("test_booking_as_provider")
        #create a patient to be dummy provider
        providerObj = system.get_patient("jack@gmail.com")
        assert(providerObj.is_provider() == False)

        centreObj = system.get_centre("USYD Health Service")
        assert(centreObj.is_centre() == True)

        userObj = system.get_patient("isaac@gmail.com")
        assert(userObj.is_provider() == False)

        datetimeObj = datetime.datetime(2018,1,1,10,30)
        note = "I'm drowning, help me!"
        referral_id = 0 

        try:
            apmt = system.add_current_appointment(userObj, providerObj, centreObj, datetimeObj, note, referral_id)
        except BookingError as be:
            print(be.msg)
            #assert(be.msg =="Booking error occured with fields: user")
            assert(True)
        else:
            assert(False)
        pass

    def test_provider_not_exist(self):
        print ("test_booking_when_provider_not_exist")
        centreObj = system.get_centre("USYD Health Service")
        assert(centreObj.is_centre() == True)

        userObj = system.get_provider("toby@gmail.com")
        assert(userObj.is_provider() == True)

        datetimeObj = datetime.datetime(2018,1,1,10,30)
        note = "I'm a doctor, I also get sick!"
        referral_id = 0 

        try:
            apmt = system.add_current_appointment(userObj, None, centreObj, datetimeObj, note, referral_id)
        except BookingError as be:
            print(be.msg)
            #assert(be.msg =="Booking error occured with fields: Unknown provider or specialist, Provider/Centre Relation")
            assert(True)
           
        else:
            assert(False)
        pass

    def test_centre_not_exist(self):
        print ("test_booking_when_centre_not_exist")

        providerObj = system.get_provider("toby@gmail.com")
        assert(providerObj.is_provider() == True)

        centreObj = None
        
        userObj = system.get_patient("isaac@gmail.com")
        assert(userObj.is_provider() == False)

        datetimeObj = datetime.datetime(2018,1,1,10,30)
        note = "I'm bleeding, help me!"
        referral_id = 0 

        try:
            apmt = system.add_current_appointment(userObj, providerObj, centreObj, datetimeObj, note, referral_id)
        except BookingError as be:
            print(be.msg)
            #assert(be.msg =="Booking error occured with fields: user")
            assert(True)
        else:
            assert(False)
        pass

    def test_provider_with_wrong_centre(self):

        print ("test_booking_when_centre_not_exist")

        providerObj = system.get_provider("toby@gmail.com")
        assert(providerObj.is_provider() == True)

        centreObj = system.get_centre("Prince of Wales Hospital")
        assert(centreObj.is_centre() == True)
        
        userObj = system.get_patient("isaac@gmail.com")
        assert(userObj.is_provider() == False)

        datetimeObj = datetime.datetime(2018,1,1,10,30)
        note = "I'm bleeding, help me!"
        referral_id = 0 

        try:
            apmt = system.add_current_appointment(userObj, providerObj, centreObj, datetimeObj, note, referral_id)
        except BookingError as be:
            print(be.msg)
            #assert(be.msg =="Booking error occured with fields: user")
            assert(True)
        else:
            assert(False)
        pass
        pass

    def test_provider_cannot_book(self):
        print ("test_provider_cannot_book")

        providerObj = system.get_provider("gary@gmail.com")
        assert(providerObj.is_provider() == True)

        centreObj = system.get_centre("USYD Health Service")
        assert(centreObj.is_centre() == True)

        datetimeObj = datetime.datetime(2018,1,1,10,30)
        note = "I'm a doctor, please help me too doctor!"
        referral_id = 0 

        try:
            apmt = system.add_current_appointment(providerObj, providerObj, centreObj, datetimeObj, note, referral_id)
        except BookingError as be:
            print(be.msg)
            #assert(be.msg =="Booking error occured with fields: double book warning")
            assert(True)
        else:
            assert(False)
        

    def test_successful_appointment_with_specialist(self):
        print ("test_booking_appointment_with_specialist")
        #add a new appointment with same detail from above 
        providerObj = system.get_provider("huss@gmail.com")
        assert(providerObj.is_provider() == True)
        assert(providerObj.is_specialist() == True)

        centreObj = system.get_centre("UNSW Health Service")
        assert(centreObj.is_centre() == True)

        userObj = system.get_patient("paige@gmail.com")
        assert(userObj.is_provider() == False)

        datetimeObj = datetime.datetime(2018,1,1,10,30)
        note = "I'm has tumour, please help me doctor!"
        referral_id = 0 

        try:
            apmt = system.add_current_appointment(userObj, providerObj, centreObj, datetimeObj, note, referral_id)
        except BookingError as be:
            assert(False)
        else:
            assert(apmt.patient.full_name == userObj.full_name)
            assert(apmt.provider == providerObj)
            assert(apmt.healthcare_centre == centreObj)
            assert(apmt.datetime == datetimeObj)
            assert(apmt.patient_note == note)
            apmt.patient_note = None
            assert(apmt.patient_note == None)
            pass

class TestViewPatientHistory(object):
    def setup_method(self):
        self.system = system 

    def test_no_current_appointment(self):

        pass

    def test_multiple_current_appointment(self):
        pass

    def test_multiple_pass_appointment(self):
        pass

    def test_current_and_pass_appointment(self):
        pass

class TestProviderConsultation(object):
    def setup_method(self):
        self.system = system 

    def test_no_current_appointment(self):

        pass

    def test_multiple_current_appointment(self):
        print ("test_successful_booking_appointment")

        providerObj = system.get_provider("gary@gmail.com")
        assert(providerObj.is_provider() == True)

        centreObj = system.get_centre("USYD Health Service")
        assert(centreObj.is_centre() == True)

        userObj = system.get_patient("isaac@gmail.com")
        assert(userObj.is_provider() == False)

        datetimeObj = datetime.datetime(2018,3,1,10,30)
        note = "I'm dying, please help me doctor!"
        referral_id = 0 

        apmt = system.add_current_appointment(userObj, providerObj, centreObj, datetimeObj, note, referral_id)
        assert(apmt.patient.full_name == userObj.full_name)
        assert(apmt.provider == providerObj)
        assert(apmt.healthcare_centre == centreObj)
        assert(apmt.datetime == datetimeObj)
        assert(apmt.patient_note == note)
        apmt.patient_note = None
        assert(apmt.patient_note == None)

        pass

    def test_consult_current_appointment(self):

        pass

    def test_edit_pass_appointment(self):
        providerObj = system.get_provider("toby@gmail.com")
        curr_apmts = system.get_current_appointments(providerObj)
        for curr_apmt in curr_apmts:
            system.move_appointment(curr_apmt)
        past_apmts = system.get_past_appointments(providerObj)
        assert past_apmts == curr_apmts 
        pass

    def test_consult_messages(self):
        providerObj = system.get_provider("toby@gmail.com")
        centreObj = system.get_centre("Sydney Children Hospital")
        userObj = system.get_patient("jack@gmail.com")
        datetimeObj = datetime.datetime(2018,1,2,10,30)
        note = "I'm very sick, please help me doctor!"
        referral_id = 0 
        apmt = system.add_current_appointment(userObj, providerObj, centreObj, datetimeObj, note, referral_id)
        medication = ""
        comment = ""
        apmt.document_consultation(medication, comment)
        assert apmt.provider_comment == comment
        assert apmt.provider_medication == medication
        medication_1 = "Panadol"
        comment_1 = "Fever"
        apmt.document_consultation(medication, comment)
        assert apmt.provider_comment == comment
        assert apmt.provider_medication == medication
