from lib.rating import Rating
import copy

class RatingManager():

    def __init__(self):
        self._ratings = []

    @property
    def ratings(self):
        return self._ratings

    def add_rating(self, service, patient, value):
        patient = copy.copy(patient)
        rating = Rating(patient, int(value));
        for r in self._ratings:
            if (r.patient.email_address == rating.patient.email_address):
                self._ratings.remove(r)
                r.remove_data(service)
        self._ratings.append(rating)
        rating.append_data(service)

    def calculate_average_rating(self):
        sum = 0
        if len(self._ratings) == 0:
            return None;
        for rating in self._ratings:
            sum += rating.value
        average = sum / len(self._ratings)
        average = float("{0:.1f}".format(average))
        return average
