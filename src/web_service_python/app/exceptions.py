class ProductNotFoundException(Exception):
    """ Exception raised when a product is not found """
    pass

class ProductAlreadyExistsException(Exception):
    """ Exception raised when a product already exists """
    pass

class InvalidBusinessRuleException(Exception):
    """ Exception raised when an invalid business rule fails """
    pass

class InvalidProductDataException(Exception):
    """ Exception raised when an invalid product data fails """
    pass