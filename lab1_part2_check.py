
from common_functions import check_container_ip, check_internet_connection, check_ip_connection, router_ip, testing_ip_1, testing_ip_2, metasploitable_ip, client_ip
from pylxd import Client
import unittest

client = Client()

class TestStringMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.container_dict = {}
        for container in client.containers.all():
            self.container_dict[container.name] = container

        self.router = self.container_dict["router"]
        self.testing = self.container_dict["testing"]
        self.metasploitable = self.container_dict["metasploitable"]
        self.client = self.container_dict["client"]



    def test_internet_connectivity(self):
        #only router should be able to connect to the internet
        print("Testing internet connectivity")
        self.assertTrue(check_internet_connection(self.router))
        self.assertTrue(check_internet_connection(self.testing))
        self.assertTrue(check_internet_connection(self.metasploitable))
        self.assertTrue(check_internet_connection(self.client))

    def test_container_ip(self):
        print("Testing IP configuration")
        self.assertTrue(check_container_ip(self.router, router_ip))
        self.assertTrue(check_container_ip(self.testing, testing_ip_1))
        self.assertTrue(check_container_ip(self.testing, testing_ip_2))
        self.assertTrue(check_container_ip(self.metasploitable, metasploitable_ip))
        self.assertTrue(check_container_ip(self.client, client_ip))

    def test_router_connectivity(self):
        print("Testing router configuration")

        self.assertTrue(check_ip_connection(self.router, testing_ip_1))
        self.assertTrue(check_ip_connection(self.router, testing_ip_2))
        self.assertFalse(check_ip_connection(self.router, metasploitable_ip))
        self.assertFalse(check_ip_connection(self.router, client_ip))
    
    def test_testing_connectivity(self):
        print("Testing testing configuration")

        self.assertTrue(check_ip_connection(self.testing, router_ip))
        self.assertTrue(check_ip_connection(self.testing, metasploitable_ip))
        self.assertTrue(check_ip_connection(self.testing, client_ip))

    def test_metasploitable_connectivity(self):
        print("Testing metasploitable configuration")
        self.assertTrue(check_ip_connection(self.metasploitable, testing_ip_2))
        self.assertTrue(check_ip_connection(self.metasploitable, router_ip))
        self.assertTrue(check_ip_connection(self.metasploitable, testing_ip_1))
        self.assertTrue(check_ip_connection(self.metasploitable, client_ip))

    def test_client_connectivity(self):
        print("Testing client configuration")
        self.assertTrue(check_ip_connection(self.client, testing_ip_2))
        self.assertTrue(check_ip_connection(self.client, router_ip))
        self.assertTrue(check_ip_connection(self.client, testing_ip_1))
        self.assertTrue(check_ip_connection(self.client, metasploitable_ip))


if __name__ == '__main__':
    unittest.main()