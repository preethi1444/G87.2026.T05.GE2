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
        #ECV11 between 10-30 chars
        if len(project_description) < 10 or len(project_description) > 30:
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
        # budget between 50000 and 1000000
        if budget < 50000 or budget > 1000000.00:
            raise EnterpriseManagementException("Invalid budget")

        #ECV22 only 2 decimals allowed
        if round(budget, 2) != budget:
            raise EnterpriseManagementException("Invalid decimals for budget")

        # SUCCESS PATH: Register and Save
        #ECV26
        fp = os.path.join(os.path.dirname(__file__), "corporate_operations.json")
        if os.path.exists(fp):
            with open(fp, "r", encoding="utf-8") as f:
                try: data = json.load(f)
                except json.decoder.JSONDecodeError:
                    data=[]
        else:
            data=[]

        #ECV28 duplicate check
        for rec in data:
            if rec["company cif"] == company_cif and rec["project_acronym"] == project_acronym:
                raise EnterpriseManagementException("Project already exists")

        #ECV24,25,26 returning ID
        new_proj = EnterpriseProject(company_cif, project_acronym, project_description,
                                        department, date, budget)
        data.append(new_proj.to_json())
        with open(fp, "w", encoding="utf-8") as f: json.dump(data, f, indent=4)

        return new_proj.project_id



    @staticmethod
    def validate_cif(cif: str):
        #ECV1 check string
        if not isinstance(cif, str):
            return False

        #ECV2 only 9 chars
        if len(cif) !=9:
            return False
        return True
