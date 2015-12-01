"""
Test suite for the Device class
"""

# Python standard library modules
import unittest

# this package local modules
from Module11.device import Device


class DeviceTests(unittest.TestCase):
    """Test suite for the `devices.py` module, created by subclassing
    the unittest.TestCase class.

    The individual tests are defined with methods whose names start with
    the letters 'test'. This naming convention informs the test runner
    about which methods represent tests.

    The setUp() and tearDown() methods allow to define instructions
    that will be executed before and after each test method.

    For each test method defined within this class a separate class instance
    will be created to run the method, so a new fixture is created for each
    test.
    """

    # Method that is used to construct the test's environment ('fixture'),
    # is called immediately before calling the test method.
    # Overrides TestCase.setUp() method.
    # Allocates Device object in this example.
    def setUp(self):
        self.device = Device(name='Router1', os_type='IOS-XR')

    # Method that is used for deconstructing the test's environment
    # constructed with the setUp method, is called immediately after
    # the test method has been called and the result recorded.
    # Overrides TestCase.tearDown() method.
    # Does nothing in this example.
    def tearDown(self):
        pass

    # The test method (executes a specific test case)
    # Any member function whose name begins with the 'test' is a test method.
    def test_device_get_name(self):
        self.assertEqual(self.device.name, 'Router1')

    # The test method (executes a specific test case)
    def test_device_get_os_type(self):
        self.assertEqual(self.device.os_type, 'IOS-XR')

    # The test method (executes a specific test case)
    def test_device_get_ip_address(self):
        self.assertIsNone(self.device.ip_addr)

    # The test method (executes a specific test case)
    def test_device_set_ip_address(self):
        value = '10.0.0.1'
        self.device.ip_addr = value
        self.assertEqual(self.device.ip_addr, value)

    # The test method (executes a specific test case)
    def test_device_get_interfaces(self):
        self.assertIsInstance(self.device.interfaces, list)

    # The test method (executes a specific test case)
    def test_device_set_interfaces(self):
        iflist = ['Lo0', 'Mg0/0/CPU0/0', 'Gi0/0/0/0',
                  'Gi0/0/0/1', 'Gi0/0/0/2', 'Gi0/0/0/3']
        self.device.interfaces = iflist
        self.assertEqual(self.device.if_count, len(iflist))
        self.assertListEqual(self.device.interfaces, iflist)


if __name__ == "__main__":
    # The unittest.main() runs the standard test loader to find tests
    # in the current module, and all of the discovered tests are executed
    # one after the other
    unittest.main()
