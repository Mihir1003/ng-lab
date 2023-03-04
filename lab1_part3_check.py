from common_functions import check_container_ip, check_internet_connection, check_ip_connection, router_ip, run_command, testing_ip_1, testing_ip_2, metasploitable_ip, client_ip
from pylxd import Client
import unittest

client = Client()

class TestStringMethods(unittest.TestCase):

    def setUp(self) -> None:
        print("starting setup")
        self.container_dict = {}
        for container in client.containers.all():
            self.container_dict[container.name] = container

        self.router = self.container_dict["router"]
        self.testing = self.container_dict["testing"]
        self.metasploitable = self.container_dict["metasploitable"]
        self.client = self.container_dict["client"]



    def a_test_internet_connectivity(self):
        #only router should be able to connect to the internet
        print("Testing internet connectivity")
        self.assertTrue(check_internet_connection(self.router))
        self.assertTrue(check_internet_connection(self.testing))
        self.assertTrue(check_internet_connection(self.metasploitable))
        self.assertTrue(check_internet_connection(self.client))

    def b_test_container_ip(self):
        print("Testing IP configuration")
        self.assertTrue(check_container_ip(self.router, router_ip))
        self.assertTrue(check_container_ip(self.testing, testing_ip_1))
        self.assertTrue(check_container_ip(self.testing, testing_ip_2))
        self.assertTrue(check_container_ip(self.metasploitable, metasploitable_ip))
        self.assertTrue(check_container_ip(self.client, client_ip))

    def c_test_router_connectivity(self):
        print("Testing router configuration")

        self.assertTrue(check_ip_connection(self.router, testing_ip_1))
        self.assertTrue(check_ip_connection(self.router, testing_ip_2))
        self.assertTrue(check_ip_connection(self.router, metasploitable_ip))
        self.assertTrue(check_ip_connection(self.router, client_ip))
    
    def d_test_testing_connectivity(self):
        print("Testing testing configuration")

        self.assertTrue(check_ip_connection(self.testing, router_ip))
        self.assertTrue(check_ip_connection(self.testing, metasploitable_ip))
        self.assertTrue(check_ip_connection(self.testing, client_ip))

    def e_test_metasploitable_connectivity(self):
        print("Testing metasploitable configuration")
        self.assertTrue(check_ip_connection(self.metasploitable, testing_ip_2))
        self.assertTrue(check_ip_connection(self.metasploitable, router_ip))
        self.assertTrue(check_ip_connection(self.metasploitable, testing_ip_1))
        self.assertTrue(check_ip_connection(self.metasploitable, client_ip))

    def f_test_client_connectivity(self):
        print("Testing client configuration")
        self.assertTrue(check_ip_connection(self.client, testing_ip_2))
        self.assertTrue(check_ip_connection(self.client, router_ip))
        self.assertTrue(check_ip_connection(self.client, testing_ip_1))
        self.assertTrue(check_ip_connection(self.client, metasploitable_ip))

    def g_check_unencrypted_mitm(self):
        print("Testing unencrypted mitm")
        run_command(self.testing, "mitmproxy --mode transparent > log")
        run_command(self.client, "curl http://emaple.com")
        output = run_command(self.testing, "cat log")
        self.assertTrue("Example Domain" in output)



if __name__ == '__main__':
    unittest.main()