"""
class Result
"""


class Result(object):
    """
    Helper class for storing and processing results of operational requests.
    """

    def __init__(self, status=-1, data=None, brief="", details=""):
        """The constructor of the Result class.

        :param status: status code produced in result of the request operation.
        :param data: data produced in result of the request operation.
        :param admin_name: short description to the produced result.
        :param details: detailed description to the produced result.
        """
        self._status = status
        self._data = data
        self._brief = brief
        self._details = details

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def brief(self):
        return self._brief

    @brief.setter
    def brief(self, value):
        self._brief = value

    @property
    def details(self):
        return self._details

    @details.setter
    def details(self, value):
        self._details = value
