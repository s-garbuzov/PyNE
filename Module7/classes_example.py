#!/usr/bin/env python

# Python Classes (Examples)


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

        self._vendor = vendor
        self._os_type = os_type
        self._desription = desription

    def get_manufacturer(self):
        """
        Method that returns information about the device
        manufacturer (gets the value of '_vendor' class property).
        """
        return self._vendor

    def get_os_type(self):
        """
        Method that returns information about OS type used on
        the device (gets the value of '_os_type' class property).
        """
        return self._os_type.upper()

    def get_description(self):
        """
        Method that returns device description information
        (gets value of '_desription' class property).
        """
        return self._desription

    def set_description(self, text_str):
        """
        Method that stores device description information
        (sets the value of '_desription' class property).
        """
        self._desription = text_str


# Subclass of the 'NetworkDevice' base class
# Python provides for inheritance, by which a class can extend the
# facilities of another class (or multiple other classes)
class CiscoIOS(NetworkDevice):
    """
    Class representing an instance of a Cisco network device running IOS.

    Defines device specific methods.
    """

    def __init__(self, ip_addr, port=22, admin_name="", admin_password=""):
        """Constractor method of the class
            :param addr: device's management IP address  (mandatory).
            :param port: Protocol port number to use while connecting
                         to the device (optional, default is 22).
            :param admin_name: device administrator user name (optional,
                               default is empty string).
            :param admin_pswd: device administrator password (optional,
                               default is empty string).
            :param description: textual description to associate with the
                                device (optional).
            :return: The newly created object instance of the class.
        """

        # Invoke the superclass initialization method to initialize
        # inherited attributes
        NetworkDevice.__init__(self, 'Cisco', 'ios')

        # Initialize this class specific attributes
        self._ip_addr = ip_addr
        self._port = port
        self._admin_name = admin_name
        self._admin_pswd = admin_password
        self._remote_shell = None

    def __repr__(self):
        """ Method that overloads  Python's build-in __repr__ method"""
        return "Cisco IOS device(%s)" % self._ip_addr

    def get_addr(self):
        return self._ip_addr

    def get_port(self):
        return self._port

    def get_rsh(self):
        """
        Method that returns a reference to the device management session
        (remote shell instance running on the device)
        """
        return self._remote_shell

    def connect(self):
        """Initiate management session on the device."""
        pass

    def disconnect(self):
        """Terminate management session on the device."""
        pass

    def get_firmware_version(self):
        """
        Class specific method that retrieves and returns
        the firmware version from the device.
        """
        pass


# Another subclass of the 'NetworkDevice' base class
class CiscoEOS(NetworkDevice):
    """
    Class representing an instance of a Cisco network device running EOS.

    Defines device specific methods.
    """

    def __init__(self, ip_addr, port=22, admin_name="", admin_password=""):
        """Constractor method of the class
            :param addr: device's management IP address  (mandatory).
            :param port: Protocol port number to use while connecting
                         to the device (optional, default is 22).
            :param admin_name: device administrator user name (optional,
                               default is empty string).
            :param admin_pswd: device administrator password (optional,
                               default is empty string).
            :param description: textual description to associate with the
                                device (optional).
            :return: The newly created object instance of the class.
        """

        # Invoke the superclass initialization method to initialize
        # inherited attributes
        NetworkDevice.__init__(self, 'Cisco', 'eos')

        # Initialize this class specific attributes
        self._ip_addr = ip_addr
        self._port = port
        self._admin_name = admin_name
        self._admin_pswd = admin_password
        self._remote_shell = None

    def __repr__(self):
        """ Method that overloads  Python's build-in method __repr__"""
        return "Cisco EOS device(%s)" % self._ip_addr

    def get_addr(self):
        return self._ip_addr

    def get_port(self):
        return self._port


# Create first object (CiscoIOS class instantiation)
cisco_ios = CiscoIOS('192.0.2.1')
# Call for the method that is inherited from the superclass
cisco_ios.set_description("Core router")

print "\n"

# Call Python's built-in function that returns canonical string
# representation of the object. Since __repr__ method is overloaded
# in the object we will see the customized output string
print "Object      : %s" % repr(cisco_ios)

# Call for the methods that are inherited from the superclass
print "Description : %s" % cisco_ios.get_description()
print "Manufacturer: %s" % cisco_ios.get_manufacturer()
print "OS type     : %s" % cisco_ios.get_os_type()

# Call for the object instance methods
print "IP address  : %s" % cisco_ios.get_addr()
print "Port:       : %s" % cisco_ios.get_port()

# Create second object (CiscoEOS class instantiation)
cisco_eos = CiscoEOS('192.0.2.2')
# Call for the method that is inherited from the superclass
cisco_eos.set_description("Edge router")

print "\n"

# Call Python's built-in function that returns canonical string
# representation of the object. Since __repr__ method is overloaded
# in the object we will see the customized output string
print "Object      : %s" % repr(cisco_eos)

# Call for the methods that are inherited from the superclass
print "Description : %s" % cisco_eos.get_description()
print "Manufacturer: %s" % cisco_eos.get_manufacturer()
print "OS type     : %s" % cisco_eos.get_os_type()

# Call for the object instance methods
print "IP address  : %s" % cisco_eos.get_addr()
print "Port:       : %s" % cisco_eos.get_port()

print "\n"
