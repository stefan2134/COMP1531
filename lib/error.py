class LoginError(Exception):
    
    def __init__(self, errors, msg=None):
        if msg is None:
            self.msg = "Login error occured with fields: %s"%(','.join(errors))
        super().__init__(msg)
        self.errors = errors
        
class SearchError(Exception):
    def __init__(self, message):
        self._message = message

    @property
    def message(self):
        return self._message
        
class BookingError(Exception):

    def __init__(self, errors, msg=None):
        if msg is None:
            self.msg = "Booking error occured with fields: %s"%(', '.join(errors))
        super().__init__(msg)
        self.errors = errors


