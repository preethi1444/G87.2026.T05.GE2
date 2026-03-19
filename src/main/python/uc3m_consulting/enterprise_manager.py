import json
import os
from .enterprise_management_exception import EnterpriseManagementException
from .enterprise_project import EnterpriseProject
from datetime import datetime

class EnterpriseManager:
    def __init__(self):
        pass

    def register_project(self, company_cif, project_acronym, project_description, department, date, budget):
        # 1. Budget Format Check (TC21)
        if not isinstance(budget, float):
            raise EnterpriseManagementException("Invalid budget format")

        # 2. CIF Length (TC15) (ECV1-ECV6)
        if not self.validate_cif(company_cif):
            raise EnterpriseManagementException("Invalid CIF length")

        # 3. Duplicate Check (TC25) - This will work now!
        #if project_acronym in self.registered_acronyms:
            raise EnterpriseManagementException("Project already exists")

        # 4. Acronym Length (TC20)
        # ECV8 need to check string between 5 and 10 chars
        if len(project_acronym) <5 or len(project_acronym) > 10:
            raise EnterpriseManagementException("Invalid acronym length")

        #ECV9 can only have letters A-Z or numbers 0-9
        for ch in project_acronym:
            if not (ch.isupper() or ch.isdigit()):
                raise EnterpriseManagementException("Invalid acronym")

        # 5. Description Length (TC24)
        if len(project_description) < 10:
            raise EnterpriseManagementException("Description too short")

        # 6. Department Validation (TC16)
        allowed_departments = ["HR", "FINANCE", "LEGAL", "LOGISTICS"]
        if department not in allowed_departments:
            raise EnterpriseManagementException("Invalid department")

        # 7. Date & Year Validation (TC22, TC23)
        try:
            req_date = datetime.strptime(date, "%d/%m/%Y")
            if req_date < datetime.now():
                raise EnterpriseManagementException("Date cannot be in the past")
            if req_date.year < 2025 or req_date.year > 2027:
                raise EnterpriseManagementException("Invalid year")
        except ValueError:
            raise EnterpriseManagementException("Invalid date format")

        # 8. Budget Range (TC17)
        if budget < 0 or budget > 1000000.00:
            raise EnterpriseManagementException("Invalid budget")

        # SUCCESS PATH: Register and Save
        self.registered_acronyms.append(project_acronym)
        new_project = EnterpriseProject(company_cif, project_acronym, project_description,
                                        department, date, budget)

        return new_project.project_id

    @staticmethod
    def validate_cif(cif: str):
        """RETURNs TRUE IF THE IBAN RECEIVED IS VALID SPANISH IBAN,
        OR FALSE IN OTHER CASE"""
        return True
