from common_functions import check_container_ip, check_internet_connection, check_ip_connection, router_ip, run_command, testing_ip_1, testing_ip_2, metasploitable_ip, client_ip
from lab1_part2_check import TestLab1Part2
from pylxd import Client
import unittest

client = Client()

class TestStringMethods(TestLab1Part2):
  
    def test_z_check_unencrypted_mitm(self):
        print("Testing unencrypted mitm")
        run_command(self.testing, "mitmproxy --mode transparent > log")
        run_command(self.client, "curl http://emaple.com")
        output = run_command(self.testing, "cat log")
        self.assertTrue("Example Domain" in output)



if __name__ == '__main__':
    unittest.main()