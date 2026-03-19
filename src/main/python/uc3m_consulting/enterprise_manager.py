from .enterprise_management_exception import EnterpriseManagementException
from .enterprise_project import EnterpriseProject
from datetime import datetime

class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    def register_project(self, company_cif, project_acronym, project_description, department, date, budget):
        if not isinstance(budget, float):
            raise EnterpriseManagementException("Invalid budget format")

        if len(company_cif) != 9:
            raise EnterpriseManagementException("Invalid CIF length")

        if len(project_acronym) > 10:
            raise EnterpriseManagementException("Invalid acronym length")

       # if len(project_description) < 10:
        #    raise EnterpriseManagementException("Description too short")

        allowed_departments = ["HR", "FINANCE", "LEGAL", "LOGISTICS"]
        if department not in allowed_departments:
            raise EnterpriseManagementException("Invalid department")

        try:
            req_date = datetime.strptime(date, "%d/%m/%Y")
            if req_date < datetime.now():
                raise EnterpriseManagementException("Date cannot be in the past")
            if req_date.year < 2025 or req_date.year > 2027:
                raise EnterpriseManagementException("Invalid year")
        except ValueError:
            raise EnterpriseManagementException("Invalid date format")

        if budget < 0 or budget > 1000000.00:
            raise EnterpriseManagementException("Invalid budget")

        new_project = EnterpriseProject(company_cif, project_acronym, project_description,
                                        department, date, budget)

        return new_project.project_id

    @staticmethod
    def validate_cif(cif: str):
        """RETURNs TRUE IF THE IBAN RECEIVED IS VALID SPANISH IBAN,
        OR FALSE IN OTHER CASE"""
        return True
