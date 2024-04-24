import sys
sys.path.append('/nfs/site/disks/vmisd_vclp_efficiency/rcg/server/fullServer/venvRcg/lib/python3.11/site-packages')
import typer
import unittest
from unittest.mock import patch
from timingCommands import *  # Import your function from the module you defined it in
from ptServerDatabasemysql import *
import globalVariable
from io import StringIO

class TestCurrentCorner(unittest.TestCase):
    def test_current_corner_output(self):
        globalVariable.corner = "sifunctional_typ_0p58v_85c_typical_CCworst_85C_max"
        captured_output = StringIO()
        sys.stdout = captured_output
        current_corner()
        sys.stdout = sys.__stdout__
        printed_output = captured_output.getvalue().strip()
        self.assertEqual(printed_output, "The current corners is: sifunctional_typ_0p58v_85c_typical_CCworst_85C_max")

    def test_load_corner_output(self):
        globalVariable.corner = "sifunctional_typ_0p58v_85c_typical_CCworst_85C_max"  # Set an initial corner value
        corner_to_load = "sifunctional_typ_0p85v_85c_typical_CCworst_85C_max"
        # Call load_corner function
        with patch('sys.stdout', new=StringIO()) as fake_output:
            result = load_corner(corner_to_load)
        # Assertions
        #mock_print.assert_called_with("changed the corner to ", corner_to_load)
        self.assertEqual(result, corner_to_load)
        self.assertEqual(globalVariable.corner, corner_to_load)

    @patch('builtins.print')
    def test_current_work_week(self, mock_print):
        # Set up
        globalVariable.runName = "WW4p2"
        # Call the function
        current_work_week()
        # Assertion
        self.assertNotEqual(globalVariable.runName,"default")


class TestConnectMySql(unittest.TestCase):
    def test_connection(self):
        connection = connectMySql()
        self.assertIsNotNone(connection)
        connection.close()


if __name__ == '__main__':
    unittest.main()