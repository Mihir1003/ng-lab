
from common_functions import run_command,container_dict


if __name__ == '__main__':
    run_command(container_dict["testing"], "sudo apt-get update && sudo apt-get install mitmproxy")
    run_command(container_dict["testing"], "sudo iptables -t nat -A PREROUTING -i enp0s9 -p tcp --dport 80 -j REDIRECT --to-port 8080 ")
    run_command(container_dict["testing"], "sudo iptables -t nat -A PREROUTING -i enp0s9 -p tcp --dport 443 -j REDIRECT --to-port 8080")
    