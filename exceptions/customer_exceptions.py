#needs implementation (check if valid european vat format)
class WrongVATNumberError(Exception):
    pass

class CustomerNotFoundError(Exception):
    pass

class CustomerAlreadyExistsError(Exception):
    pass