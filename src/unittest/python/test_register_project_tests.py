import unittest
from uc3m_consulting.enterprise_manager import EnterpriseManager
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

# Format: from folder.file import Class
class TestRegisterProject(unittest.TestCase):
    """Test suite for the register_project method (Method 1)"""

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
                company_cif="A12345674",
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
                company_cif="A12345674",
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
                company_cif="A12345674",
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
                company_cif="A12345674",
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
                company_cif="A12345674",
                project_acronym="PROJECTTOOLONG",
                project_description="Main Research Proj",
                department="HR",
                date="15/06/2026",
                budget=100000.00
            )
        self.assertEqual(str(context.exception), "Invalid acronym length")

    def test_tc21_budget_no_decimals(self):
        """TC21: Budget with 0 decimals"""
        my_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as context:
            my_manager.register_project(
                company_cif="A12345674",
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
                company_cif="A12345674",
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
                company_cif="A12345674",
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
                company_cif="A12345674",
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
            "A12345674", "PROJ01", "Valid Description Long", "HR", "15/06/2026", 100000.00
        )

        # Second registration with same acronym (Should fail)
        with self.assertRaises(EnterpriseManagementException) as context:
            my_manager.register_project(
                "A12345674", "PROJ01", "Different Desc But Same Acronym", "HR", "15/06/2026", 100000.00
            )
        self.assertEqual(str(context.exception), "Project already exists")

    def test_tc26_md5_format(self):
        """TC26: Verify Project ID is a valid 32-char MD5 string"""
        my_manager = EnterpriseManager()
        project_id = my_manager.register_project(
            "A12345674", "PROJVALID", "This is a long valid desc", "HR", "15/06/2026", 100000.00
        )
        self.assertEqual(len(project_id), 32)
        self.assertTrue(all(c in "0123456789abcdef" for c in project_id))

if __name__ == '__main__':
    unittest.main()