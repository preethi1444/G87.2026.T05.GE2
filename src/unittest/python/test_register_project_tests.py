import unittest
import os
from freezegun import freeze_time
from src.main.python.uc3m_consulting.enterprise_manager import EnterpriseManager
from src.main.python.uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

# Format: from folder.file import Class
class TestRegisterProject(unittest.TestCase):
    """Test suite for the register_project method (Method 1)"""

    def setUp(self):
        # clearing JSON before each test to ensure no clashes
        self.mgr = EnterpriseManager()
        fp = os.path.join(os.path.dirname(__file__), "../../main/python/uc3m_consulting/corporate_operations.json")

        if os.path.exists(fp):
            os.remove(fp)

    # TC1 - Baseline valid case
    @freeze_time("2025-01-01")
    def test_tc1_valid_baseline(self):
        res = self.mgr.register_project("A12345678", "PROJ01", "Research Project 2026", "HR", "15/06/2026", 100000.00)
        self.assertIsInstance(res, str)
        self.assertEqual(len(res), 32)
        self.assertTrue(all(c in "0123456789abcdef" for c in res))

    # TC2 - Acronym too short (4)
    @freeze_time("2025-01-01")
    def test_tc2_acr_short(self):
        with self.assertRaises(EnterpriseManagementException):
            self.mgr.register_project("A12345678", "PRJ1", "Main Research Proj", "HR", "15/06/2026", 100000.00)

    # TC3 - CIF too long (10)
    @freeze_time("2025-01-01")
    def test_tc3_cif_long(self):
        with self.assertRaises(EnterpriseManagementException):
            self.mgr.register_project("A123456749", "PROJ01", "Main Research Proj", "HR", "15/06/2026", 100000.00)

    # TC4 - Dept in lowercase
    @freeze_time("2025-01-01")
    def test_tc4_dept_lowercase(self):
        with self.assertRaises(EnterpriseManagementException):
            self.mgr.register_project("A12345678", "PROJ01", "Main Research Proj", "hr", "15/06/2026", 100000.00)

    # TC5 - Budget just below min
    @freeze_time("2025-01-01")
    def test_tc5_budget_below_min(self):
        with self.assertRaises(EnterpriseManagementException):
            self.mgr.register_project("A12345678", "PROJ01", "Main Research Proj", "HR", "15/06/2026", 49999.99)

    # TC6 - Budget at exact max
    @freeze_time("2025-01-01")
    def test_tc6_budget_at_max(self):
        res = self.mgr.register_project("A12345678", "PROJ01", "Main Research Proj", "HR", "15/06/2026", 1000000.00)
        self.assertIsInstance(res, str)
        self.assertEqual(len(res), 32)

    # TC7 - CIF wrong checksum
    @freeze_time("2025-01-01")
    def test_tc7_wrong_checksum(self):
        with self.assertRaises(EnterpriseManagementException):
            self.mgr.register_project("A12345670", "PROJ01", "Main Research Proj", "HR", "15/06/2026", 100000.00)

    # TC8 - Desc too long (31)
    @freeze_time("2025-01-01")
    def test_tc8_desc_too_long(self):
        with self.assertRaises(EnterpriseManagementException):
            self.mgr.register_project("A12345678", "PROJ01", "Research Project Different Than Last Year's in 2025",
                                      "HR", "15/06/2026", 100000.00)

    # TC9 - Date in 2024
    def test_tc9_date_wrong(self):
        with self.assertRaises(EnterpriseManagementException):
            self.mgr.register_project("A12345678", "PROJ01", "Main Research Proj", "HR", "31/12/2024", 100000.00)

    # TC10 - Budget has more than 2 decimals
    @freeze_time("2025-01-01")
    def test_tc10_budget_more_than_2_dec(self):
        with self.assertRaises(EnterpriseManagementException):
            self.mgr.register_project("A12345678", "PROJ01", "Main Research Proj", "HR", "31/12/2024", 75.0002)

    # TC11 - Acronym at max (10)
    @freeze_time("2025-01-01")
    def test_tc11_acr_at_max(self):
        res = self.mgr.register_project("A12345678", "PROJECT001", "Main Research Proj", "HR", "31/12/2026", 100000.00)
        self.assertIsInstance(res, str)
        self.assertEqual(len(res), 32)

    # TC12 - Acronym special char
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


    def test_tc14_invalid_day_32(self):
        """TC14: Invalid Day - 32/01/2026 (Expected failure)"""
        my_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as context:
            my_manager.register_project(
                company_cif="A12345678", # Valid CIF
                project_acronym="PROJ01",
                project_description="Main Research Proj",
                department="HR",
                date="32/01/2026", # INVALID DAY
                budget=100000.00
            )
        self.assertEqual(str(context.exception), "Invalid date format")

    def test_tc15_cif_too_short(self):
            my_manager = EnterpriseManager()
            with self.assertRaises(EnterpriseManagementException) as context:
                my_manager.register_project(
                    company_cif="A1234567",  # 8 chars
                    project_acronym="PROJ01",
                    project_description="Main",
                    department="HR",
                    date="15/06/2026",
                    budget=100.0
                )
            self.assertEqual(str(context.exception), "Invalid CIF length")

    def test_tc16_invalid_department(self):
        """TC16: Invalid Department - MARKETING """
        my_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as context:
            my_manager.register_project(
                company_cif="A12345678",
                project_acronym="PROJ01",
                project_description="Main Research Proj",
                department="MARKETING",  # INVALID DEPARTMENT
                date="15/06/2026",
                budget=100000.00
            )
        self.assertEqual(str(context.exception), "Invalid department")

    def test_tc17_budget_above_max(self):
        """TC17: Budget just above max - 1,000,000.01"""
        my_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as context:
            my_manager.register_project(
                company_cif="A12345678",
                project_acronym="PROJ01",
                project_description="Main Research Proj",
                department="HR",
                date="15/06/2026",
                budget=1000000.01  # INVALID: 0.01 over the limit
            )
        self.assertEqual(str(context.exception), "Invalid budget")

    def test_tc18_description_at_min_10(self):
        """TC18: Desc at min (10) """
        my_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as context:
            my_manager.register_project(
                company_cif="A12345678",
                project_acronym="PROJ01",
                project_description="Ten Char",
                department="HR",
                date="15/06/2026",
                budget=100000.00
            )
        self.assertEqual(str(context.exception), "Description too short")

    def test_tc19_date_format_with_dots(self):
        """TC19: Date format with dots """
        my_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as context:
            my_manager.register_project(
                company_cif="A12345678",
                project_acronym="PROJ01",
                project_description="Main Research Proj",
                department="HR",
                date="15.06.2026",
                budget=100000.00
            )
        self.assertEqual(str(context.exception), "Invalid date format")

    def test_tc20_acronym_too_long(self):
        """TC20: Acronym too long"""
        my_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as context:
            my_manager.register_project(
                company_cif="A12345678",
                project_acronym="PROJECTTOOLONG",
                project_description="Main Research Proj",
                department="HR",
                date="15/06/2026",
                budget=100000.00
            )
        self.assertEqual(str(context.exception), "Invalid acronym length")

    @freeze_time("2025-01-01")
    def test_tc21_budget_no_decimals(self):
        """TC21: Budget with 0 decimals"""
        my_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as context:
            my_manager.register_project(
                company_cif="A12345678",
                project_acronym="PROJ01",
                project_description="Main Research Proj",
                department="HR",
                date="01/01/2026",
                budget=60000
            )
        self.assertEqual(str(context.exception), "Invalid budget format")

    def test_tc22_year_2028_upper_bound(self):
        """TC22: Year 2028 - Upper Bound (Invalid)"""
        my_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as context:
            my_manager.register_project(
                company_cif="A12345678",
                project_acronym="PROJ01",
                project_description="Main Research Proj",
                department="HR",
                date="01/01/2028",
                budget=100000.00
            )
        self.assertEqual(str(context.exception), "Invalid year")

    def test_tc23_date_in_past(self):
        """TC23: Date in the past """
        my_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as context:
            my_manager.register_project(
                company_cif="A12345678",
                project_acronym="PROJ01",
                project_description="Main Research Proj",
                department="HR",
                date="01/01/2025",  # PAST DATE
                budget=100000.00
            )
        self.assertEqual(str(context.exception), "Date cannot be in the past")

    def test_tc24_description_at_nine_chars(self):
        """TC24: Description at 9 chars"""
        my_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as context:
            my_manager.register_project(
                company_cif="A12345678",
                project_acronym="PROJ01",
                project_description="Nine char",  # EXACTLY 9 CHARACTERS
                department="HR",
                date="15/06/2026",
                budget=100000.00
            )
        self.assertEqual(str(context.exception), "Description too short")

    def test_tc25_duplicate_project(self):
        """TC25: Duplicate Project - Same acronym 'PROJ01' (Invalid)"""
        my_manager = EnterpriseManager()
        my_manager.register_project(
            "A12345678", "PROJ01", "Valid Description Long", "HR", "15/06/2026", 100000.00
        )

        # Second registration with same acronym (Should fail)
        with self.assertRaises(EnterpriseManagementException) as context:
            my_manager.register_project(
                "A12345678", "PROJ01", "Different Desc But Same Acronym", "HR", "15/06/2026", 100000.00
            )
        self.assertEqual(str(context.exception), "Project already exists")

    def test_tc26_md5_format(self):
        """TC26: Verify Project ID is a valid 32-char MD5 string"""
        my_manager = EnterpriseManager()
        project_id = my_manager.register_project(
            "A12345678", "PROJVALID", "This is a long valid desc", "HR", "15/06/2026", 100000.00
        )
        self.assertEqual(len(project_id), 32)
        self.assertTrue(all(c in "0123456789abcdef" for c in project_id))

if __name__ == '__main__':
    unittest.main()