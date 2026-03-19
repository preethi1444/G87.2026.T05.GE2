import unittest
import os
from freezegun import freeze_time
from src.main.python.uc3m_consulting.enterprise_manager import EnterpriseManager
from src.main.python.uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

class TestRegisterProject(unittest.TestCase):
    def setUp(self):
        #clearing JSON before each test to ensure no clashes
        self.mgr= EnterpriseManager()
        fp= os.path.join(os.path.dirname(__file__), "corporate_operations.json")

        if os.path.exists(fp):
            os.remove(fp)


    #TC1 - Baseline valid case
    @freeze_time("2025-01-01")
    def test_tc1_valid_baseline(self):
        res=self.mgr.register_project("A12345678", "PROJ01", "Research Project 2026", "HR", "15/06/2026", 100000.00)
        self.assertIsInstance(res, str)
        self.assertEqual(len(res), 32)
        self.assertTrue(all(c in "0123456789abcdef" for c in res))

    #TC2 - Acronym too short (4)
    @freeze_time("2025-01-01")
    def test_tc2_acr_short(self):
        with self.assertRaises(EnterpriseManagementException):
            self.mgr.register_project("A12345678", "PRJ1", "Main Research Proj", "HR", "15/06/2026", 100000.00)

    #TC3 - CIF too long (10)
    @freeze_time("2025-01-01")
    def test_tc3_cif_long(self):
        with self.assertRaises(EnterpriseManagementException):
            self.mgr.register_project("A123456749", "PROJ01", "Main Research Proj", "HR", "15/06/2026", 100000.00)

    #TC4 - Dept in lowercase
    @freeze_time("2025-01-01")
    def test_tc4_dept_lowercase(self):
        with self.assertRaises(EnterpriseManagementException):
            self.mgr.register_project("A12345678", "PROJ01", "Main Research Proj", "hr", "15/06/2026", 100000.00)

    #TC5 - Budget just below min
    @freeze_time("2025-01-01")
    def test_tc5_budget_below_min(self):
        with self.assertRaises(EnterpriseManagementException):
            self.mgr.register_project("A12345678", "PROJ01", "Main Research Proj", "HR", "15/06/2026", 49999.99)

    #TC6 - Budget at exact max
    @freeze_time("2025-01-01")
    def test_tc6_budget_at_max(self):
        res = self.mgr.register_project("A12345678", "PROJ01", "Main Research Proj", "HR", "15/06/2026", 1000000.00)
        self.assertIsInstance(res, str)
        self.assertEqual(len(res), 32)

    #TC7 - CIF wrong checksum
    @freeze_time("2025-01-01")
    def test_tc7_wrong_checksum(self):
        with self.assertRaises(EnterpriseManagementException):
            self.mgr.register_project("A12345670", "PROJ01", "Main Research Proj", "HR", "15/06/2026", 100000.00)

    #TC8 - Desc too long (31)
    @freeze_time("2025-01-01")
    def test_tc8_desc_too_long(self):
        with self.assertRaises(EnterpriseManagementException):
            self.mgr.register_project("A12345678", "PROJ01", "Research Project Different Than Last Year's in 2025", "HR", "15/06/2026", 100000.00)

    #TC9 - Date in 2024
    def test_tc9_date_wrong(self):
        with self.assertRaises(EnterpriseManagementException):
            self.mgr.register_project("A12345678", "PROJ01", "Main Research Proj", "HR", "31/12/2024", 100000.00)

    #TC10 - Budget has more than 2 decimals
    @freeze_time("2025-01-01")
    def test_tc10_budget_more_than_2_dec(self):
        with self.assertRaises(EnterpriseManagementException):
            self.mgr.register_project("A12345678", "PROJ01", "Main Research Proj", "HR", "31/12/2024", 75.0002)

    #TC11 - Acronym at max (10)
    @freeze_time("2025-01-01")
    def test_tc11_acr_at_max(self):
        res= self.mgr.register_project("A12345678", "PROJECT001", "Main Research Proj", "HR", "31/12/2026", 100000.00)
        self.assertIsInstance(res, str)
        self.assertEqual(len(res), 32)

    #TC12 - Acronym special char
    @freeze_time("2025-01-01")
    def test_tc12_acr_spec_char(self):
        with self.assertRaises(EnterpriseManagementException):
            self.mgr.register_project("A12345678", "PROJ!", "Main Research Proj", "HR", "31/12/2026", 100000.00)

    # TC13 - Date at end of range
    @freeze_time("2025-01-01")
    def test_tc13_date_end_of_range(self):
        res = self.mgr.register_project("A12345678", "PROJ01", "Main Research Proj", "HR", "31/12/2027", 100000.00)
        self.assertIsInstance(res, str)
        self.assertEqual(len(res), 32)

if __name__ == "__main__":
     unittest.main()