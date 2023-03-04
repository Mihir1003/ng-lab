
from pylxd import Client
import unittest

client = Client()

router_ip = "192.168.22.101"
testing_ip_1 =  "192.168.22.102" 
testing_ip_2 =  "192.168.23.102" 
metasploitable_ip = "192.168.23.103" 
client_ip = "192.168.23.104" 


def run_command(container, command):
    print(f"Running command in {container.name}: " + command)
    output = container.execute(["bash", "-c", command])
    return output.stdout

def check_ip_connection(container, ip):
    command = "ping -c 1 " + ip
    output = run_command(container, command)
    if "1 received" in output:
        return True
    else:
        return False

def check_internet_connection(container):
    command = "ping -c 1 google.com"
    output = run_command(container, command)
    if "1 received" in output:
        return True
    else:
        return False

def check_container_ip(container, ip):
    command = "ip a | grep " + ip
    output = run_command(container, command)
    if ip in output:
        return True
    else:
        return False


# test if container is able to use ICMP
def test_icmp(container):
    print("Testing ICMP")
    return check_ip_connection(container, testing_ip_1)


# test if container is able to use HTTP and HTTPS
def test_http(container,url="http://www.google.com"):
    print("Testing HTTP")
    command = "curl "+ f" {url}"
    output = run_command(container, command)
    if output == "200":
        return True
    else:
        return False
    
def test_https(container,url="https://www.google.com"):
    print("Testing HTTPS")
    command = "curl "+ f" {url}"
    output = run_command(container, command)
    if output == "200":
        return True
    else:
        return False
    
def test_dns(container):
    print("Testing DNS")
    command = "host google.com"
    output = run_command(container, command)
    if "google.com" in output:
        return True
    else:
        return False
    
def test_dhcp(container):
    print("Testing DHCP")
    command = "dhclient -v"
    output = run_command(container, command)
    if "bound to" in output:
        return True
    else:
        return False

def test_ssh(container):
    print("Testing SSH")
    command = "ssh "+ testing_ip_1
    output = run_command(container, command)
    if "Permission denied" in output:
        return True
    else:
        return False
    
#test client can use ftp
def test_ftp(container):
    print("Testing FTP")
    command = "ftp " + testing_ip_1
    output = run_command(container, command)
    if "Connected to" in output:
        return True
    else:
        return False

#client can use telnet
def test_telnet(container):
    print("Testing TELNET")
    command = "telnet " + testing_ip_1
    output = run_command(container, command)
    if "Connected to" in output:
        return True
    else:
        return False
    
#client can use smtp
def test_smtp(container):
    print("Testing SMTP")
    command = "telnet " + testing_ip_1 + " 25"
    output = run_command(container, command)
    if "Connected to" in output:
        return True
    else:
        return False

#test client cannot use pop3
def test_pop3(container):
    print("Testing POP3")
    command = "telnet " + testing_ip_1 + " 110"
    output = run_command(container, command)
    if "Connected to" in output:
        return True
    else:
        return False
    
#start simple webserver in container
def start_webserver(container):
    print("Starting webserver")
    command = "python3 -m http.server 80"
    output = run_command(container, command)
    return output




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
        self.assertFalse(check_internet_connection(self.testing))
        self.assertFalse(check_internet_connection(self.metasploitable))
        self.assertFalse(check_internet_connection(self.client))

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
        self.assertFalse(check_ip_connection(self.router, testing_ip_2))
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
        self.assertFalse(check_ip_connection(self.metasploitable, router_ip))
        self.assertTrue(check_ip_connection(self.metasploitable, testing_ip_1))
        self.assertTrue(check_ip_connection(self.metasploitable, client_ip))

    def test_client_connectivity(self):
        print("Testing client configuration")
        self.assertTrue(check_ip_connection(self.client, testing_ip_2))
        self.assertFalse(check_ip_connection(self.client, router_ip))
        self.assertTrue(check_ip_connection(self.client, testing_ip_1))
        self.assertTrue(check_ip_connection(self.client, metasploitable_ip))

    def test_protocols(self):
        self.assertTrue(test_icmp(self.client))
        self.assertTrue(test_http(self.client))
        self.assertTrue(test_https(self.client))
        self.assertTrue(test_dns(self.client))
        self.assertTrue(test_dhcp(self.client))
        self.assertTrue(test_ssh(self.client))
        self.assertFalse(test_ftp(self.client))
        self.assertFalse(test_telnet(self.client))
        self.assertFalse(test_smtp(self.client))
        self.assertFalse(test_pop3(self.client))

    # def test_webserver(self):
    #     start_webserver(self.client)
    #     self.assertFalse(test_http(self.metasploitable, "http://" + client_ip))
    #     self.assertFalse(test_https(self.metasploitable, "https://" + client_ip))
    #     self.assertTrue(check_ip_connection(self.metasploitable, client_ip))
    


if __name__ == '__main__':
    unittest.main()

