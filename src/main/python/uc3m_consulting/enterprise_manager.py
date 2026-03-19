import json
import os
from datetime import datetime
from .enterprise_management_exception import EnterpriseManagementException
from .enterprise_project import EnterpriseProject

class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def validate_cif(cif: str):
        #ECV1 check string
        if not isinstance(cif, str):
            return False

        #ECV2 must be 9 chars exactly
        #if len(cif)!=9:
        #    return False

        #EVC4 first character must be letter
        if not cif[0].isalpha():
            return False

        #ECV5 middle 7 characters must be digits
        mid=cif[1:8]
        if not mid.isdigit():
            return False

        #ECV6 last character must be valid control digit/letter
        if not cif[8].isdigit():
            return False

        #ECV3 CIF valid
        tot=sum(int(x) for x in mid)
        return (tot%10) == int(cif[8])

    def register_project(self, company_cif, project_acronym, project_description, department, date, budget):

        #checking cif
        if not self.validate_cif(company_cif):
            raise EnterpriseManagementException("Invalid Cif")

        #ECV7 is string
        if not isinstance(project_acronym, str):
            raise EnterpriseManagementException("Invalid acronym")

        #ECV8 string between 5 to 10 characters
        #if len(project_acronym)<5 or len(project_acronym)>10:
        #    raise EnterpriseManagementException("Invalid acronym length")

        #ECV9 only letters A-Z or numerical 0-9
        for ch in project_acronym:
            if not (ch.isupper() or ch.isdigit()):
                raise EnterpriseManagementException("Invalid acronym")

        #ECV10 is string
        if not isinstance(project_description, str):
            raise EnterpriseManagementException("Invalid description")

        #ECV11 is between 10-30 chars
        if len(project_description)<10 or len(project_description)>30:
            raise EnterpriseManagementException("Invalid description length")

        #ECV12 options are HR, FINANCE, LEGAL, LOGISTICS
        department_options=["HR", "FINANCE", "LEGAL", "LOGISTICS"]
        if department not in department_options:
            raise EnterpriseManagementException("Invalid department")

        #ECV13 is string
        if not isinstance(date, str):
            raise EnterpriseManagementException("Invalid date type")

        #ECV14,17,18,19
        try:
            req_date = datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            raise EnterpriseManagementException("Invalid date format")

        #ECV15 year between 2025-2027
        if req_date.year < 2025 or req_date.year > 2027:
            raise EnterpriseManagementException("Invalid year")

        #ECV20 date >= request date
        if req_date < datetime.now():
            raise EnterpriseManagementException("Date before request date")

        #ECV21 is float
        if not isinstance(budget, float):
            raise EnterpriseManagementException("Invalid budget type")

        #ECV22 only 2 decimals allowed
        if round(budget,2)!= budget:
            raise EnterpriseManagementException("Invalid budget decimal amount")


        #ECV23 number is between 50000.00 and 1000000.00
        if budget < 50000.00 or budget > 1000000.00:
            raise EnterpriseManagementException("Invalid budget amount")


        #ECV26 json file
        fp = os.path.join(os.path.dirname(__file__), "corporate_operations.json")
        if os.path.exists(fp):
            with open(fp, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.decoder.JSONDecodeError:
                    data=[]
        else:
            data=[]

        # ECV28:EnterpriseManagementException when project with same name and CIF already exists
        for rec in data:
            if rec["company_cif"] == company_cif and rec["project_acronym"] == project_acronym:
                 raise EnterpriseManagementException("Project already exists")

        #ECV24, 25, 26
        proj = EnterpriseProject(company_cif, project_acronym, project_description, department, date, budget)
        data.append(proj.to_json())
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)


        return proj.project_id