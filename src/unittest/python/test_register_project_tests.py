import unittest
# Format: from folder.file import Class
from uc3m_consulting.enterprise_manager import EnterpriseManager, EnterpriseManagementException
class TestRegisterProject(unittest.TestCase):
    """Test suite for the register_project method (Method 1)"""

    def test_tc14_invalid_day_32(self):
        """TC14: Invalid date - Day is 32 (Out of range 01-31)"""
        my_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException):
            my_manager.register_project(
                company_cif="A12345674",
                project_achronym="PROJ01",
                project_description="Main Research Proj",
                department="HR",
                date="32/01/2026", # This is the "bad" data
                budget=100000.00
            )

if __name__ == '__main__':
    unittest.main()