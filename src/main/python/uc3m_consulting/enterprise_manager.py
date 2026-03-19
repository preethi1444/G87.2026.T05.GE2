from .enterprise_management_exception import EnterpriseManagementException
from .enterprise_project import EnterpriseProject
from datetime import datetime

class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    def register_project(self, company_cif, project_acronym, project_description, department, date, budget):
        # 1. TC15: Validate CIF Length (Must be 9)
        if len(company_cif) != 9:
            raise EnterpriseManagementException("Invalid CIF length")

        # 2. TC14: Validate Date Format (Must be DD/MM/YYYY)
        try:
            # Handles "32/01/2026" by throwing a ValueError
            req_date = datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            raise EnterpriseManagementException("Invalid date format")
        new_project = EnterpriseProject(company_cif, project_acronym, project_description,
                                        department, date, budget)

        return new_project.project_id
    @staticmethod
    def validate_cif(cif: str):
        """RETURNs TRUE IF THE IBAN RECEIVED IS VALID SPANISH IBAN,
        OR FALSE IN OTHER CASE"""
        return True
