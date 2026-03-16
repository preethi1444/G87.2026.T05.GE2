import unittest
import os
from freezegun import freeze_time
from src.main.python.uc3m_consulting.enterprise_manager import EnterpriseManager
from src.main.python.uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

class TestRegisterProject(unittest.TestCase):
    def setUp(self):
        #clearing JSON before each test to ensure no clashes
        self.mgr= EnterpriseManager()
        fp= os.path.join(os.path.dirname(__file__), "../../main/python/uc3m_consulting/corporate_operations.json")

        if os.path.exists(fp):
            os.remove(fp)


    #TC1 - Baseline valid case
    @freeze_time("2025-01-01")
    def test_tc1_valid_baseline(self):
        res=self.mgr.register_project("A12345678", "PROJ01", "Research Project 2026", "HR", "15/06/2026", 100000.00)
        self.assertIsInstance(res, str)
        self.assertEqual(len(res), 32)
        self.assertTrue(all(c in "0123456789abcdef" for c in res))

if __name__ == "__main__":
     unittest.main()