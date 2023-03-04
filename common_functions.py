
from pylxd import Client
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


container_dict = {}
for container in client.containers.all():
    container_dict[container.name] = container


