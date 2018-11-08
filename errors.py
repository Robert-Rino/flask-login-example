class Errors(Exception):
    """Base class for other exceptions"""
    pass

class UserDuplicate(Errors):
   """Raised when the input value is too small"""
   messages = "User duplicated"
   
