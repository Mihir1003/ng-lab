

from common_functions import run_command,container_dict


if __name__ == '__main__':
    print(run_command(container_dict["router"], "sudo sysctl -w net.ipv4.ip_forward=1"))
    print(run_command(container_dict["testing"], "sudo sysctl -w net.ipv4.ip_forward=1"))
    print(run_command(container_dict["client"], "sudo sysctl -w net.ipv4.ip_forward=1"))
    print(run_command(container_dict["metasploitable"], "sudo sysctl -w net.ipv4.ip_forward=1"))
    print(run_command(container_dict["router"], "sudo iptables -t nat -A POSTROUTING -o enp0s3 -j MASQUERADE"))
    print(run_command(container_dict["testing"],"sudo iptables -t nat -A POSTROUTING -o enp0s8 -j MASQUERADE"))


