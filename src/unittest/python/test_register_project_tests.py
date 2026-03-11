import unittest
from uc3m_consulting import EnterpriseManager, EnterpriseManagementException

class TestRegisterProject(unittest.TestCase):
    """Test suite for the register_project method (Method 1)"""

    def test_tc01_register_project_valid(self):
        """TC01: Baseline valid case from Excel"""
        my_manager = EnterpriseManager()
        
        # Data taken directly from your Excel Row 1
        # It should return a 32-character MD5 string (the Project ID)
        result = my_manager.register_project(
            company_cif="A12345674",
            project_achronym="PROJ01",
            project_description="Research Project 2026",
            department="HR",
            date="15/06/2026",
            budget=100000.00
        )
        
        # Check if the result is a valid MD5 string (32 hex characters)
        self.assertEqual(len(result), 32)
        self.assertTrue(all(c in '0123456789abcdef' for c in result.lower()))

    def test_tc02_acronym_too_short(self):
        """TC02: Invalid case - Acronym length < 5"""
        my_manager = EnterpriseManager()
        
        # This should raise the specific Exception mentioned in section 3.1.3
        with self.assertRaises(EnterpriseManagementException):
            my_manager.register_project(
                company_cif="A12345674",
                project_achronym="PRJ1",  # Only 4 chars (Invalid)
                project_description="Main Research Proj",
                department="HR",
                date="15/06/2026",
                budget=100000.00
            )

if __name__ == '__main__':
    unittest.main()