from .enterprise_management_exception import EnterpriseManagementException
from .enterprise_project import EnterpriseProject
from datetime import datetime

class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    def register_project(self, company_cif, project_acronym, project_description, department, date, budget):
        try:
            # Python's datetime will crash if day is 32
            req_date = datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            # This is the "Valid Error" your test is looking for
            raise EnterpriseManagementException("Invalid date format")
        if not self.validate_cif(company_cif):
            raise EnterpriseManagementException("Invalid CIF length")

    @staticmethod
    def validate_cif(cif: str):
        """RETURNs TRUE IF THE IBAN RECEIVED IS VALID SPANISH IBAN,
        OR FALSE IN OTHER CASE"""
        return True
