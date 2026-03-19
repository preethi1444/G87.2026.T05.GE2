import unittest
from uc3m_consulting.enterprise_manager import EnterpriseManager
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

# Format: from folder.file import Class
class TestRegisterProject(unittest.TestCase):
    """Test suite for the register_project method (Method 1)"""

    def test_tc14_invalid_day_32(self):
        """TC14: Invalid date - Day is 32 (Out of range 01-31)"""
        my_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException):
            my_manager.register_project(
                company_cif="A12345678",
                project_acronym="PROJ01",
                project_description="Main Research Proj",
                department="HR",
                date="32/01/2026", # This is the "bad" data
                budget=100000.00
            )

    def test_tc15_invalid_cif_length_8(self):
        """TC14: Invalid CIF - Length is 8 (Expected 9)"""
        my_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as context:
            my_manager.register_project(
                company_cif="A1234567",  # Only 8 characters
                project_acronym="PROJ01",
                project_description="Main Research Proj",
                department="HR",
                date="15/06/2026",
                budget=100000.00
            )

if __name__ == '__main__':
    unittest.main()