import json
import os
from .enterprise_management_exception import EnterpriseManagementException
from .enterprise_project import EnterpriseProject

"""Module """
class EnterpriseManagementException(Exception):
    """Custom exception for UC3M Consulting Project"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def validate_cif(cif: str):
        """RETURNs TRUE IF THE IBAN RECEIVED IS VALID SPANISH IBAN,
        OR FALSE IN OTHER CASE"""
        return True


