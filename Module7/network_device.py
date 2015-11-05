

# Base class
class NetworkDevice(object):
    """
    Class representing a network device (such as router or switch)
    to be managed over network.

    Defines device independent methods.
    """

    def __init__(self, vendor, os_type, desription=None):
        """
        In Python, this method is known as the constructor, it is called
        each time an instance object is generated from the class.
            :param vendor: device manufacturer information (mandatory).
            :param os_type: OS type used on the device (mandatory).
            :param description: textual description to associate with the
                                device (optional).
            :return: The newly created object instance of the class.
        """

        self.vendor = vendor
        self.os_type = os_type
        self.desription = desription

    def get_vendor(self):
        """
        Method that returns information about the device
        manufacturer (gets the value of '_vendor' class property).
        """
        return self.vendor

    def get_os_type(self):
        """
        Method that returns information about OS type used on
        the device (gets the value of '_os_type' class property).
        """
        return self.os_type.upper()

    def get_description(self):
        """
        Method that returns device description information
        (gets value of '_desription' class property).
        """
        return self.desription

    def set_description(self, text_str):
        """
        Method that stores device description information
        (sets the value of '_desription' class property).
        """
        self.desription = text_str
