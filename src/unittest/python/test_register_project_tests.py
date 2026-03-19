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

if __name__ == '__main__':
    unittest.main()