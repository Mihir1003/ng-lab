from common_functions import run_command,container_dict



"""


ssh command:
iptables -A INPUT -p tcp --dport 22 -j ACCEPT iptables -A OUTPUT -p tcp --sport 22 -j ACCEPT Test: SSH connection keeps working
ICMP command:
iptables -A INPUT -p icmp -j ACCEPT iptables -A OUTPUT -p icmp -j ACCEPT Test: Ping different VMs and websites
NTP command:
iptables -A INPUT -p udp --dport 123 -j ACCEPT iptables -A OUTPUT -p udp --sport 123 -j ACCEPT Test: Enable NTP Time Sync on client VirtualBox and ensure time is correct
DNS Command:
          iptables -A INPUT -p <udp/tcp> --dport 1024:65535
          --sport 53 -j ACCEPT
          iptables -A INPUT -p <udp/tcp> --dport 53 --sport
          1024:65535 -j ACCEPT
          iptables -A OUTPUT -p <udp/tcp> --dport 53 --sport
          1024:65535 -j ACCEPT
          iptables -A OUTPUT -p <udp/tcp> --dport 1024:65535
          --sport 53 -j ACCEPT
Test: nslookup various websites
     
 DHCP Command:
       iptables -A INPUT -p udp --sport 67  -j ACCEPT
       #traffic from server to client
       iptables -A OUTPUT -p udp --dport 67 -j  ACCEPT
       #traffic from client to server
Test: Can connect to internet if working
HTTP Command:
iptables -A INPUT -p tcp --dport 80 -j ACCEPT iptables -A OUTPUT -p tcp --sport 80 -j ACCEPT Test: Access an http website
HTTPS Command:
iptables -A INPUT -p tcp --dport 443 -j ACCEPT iptables -A OUTPUT -p tcp --sport 443 -j ACCEPT Test: Access an https website
Setting INPUT/OUTPUT default policy to REJECT everything not specified in a rule:
iptables -P INPUT REJECT
iptables -P OUTPUT REJECT

"""



if __name__ == '__main__':

    run_command(container_dict["client"], "iptables -A INPUT -p tcp --dport 22 -j ACCEPT iptables -A OUTPUT -p tcp --sport 22 -j ACCEPT")
    run_command(container_dict["client"], "iptables -A INPUT -p icmp -j ACCEPT iptables -A OUTPUT -p icmp -j ACCEPT")
    run_command(container_dict["client"], "iptables -A INPUT -p udp --dport 123 -j ACCEPT iptables -A OUTPUT -p udp --sport 123 -j ACCEPT")
    run_command(container_dict["client"], "iptables -A INPUT -p <udp/tcp> --dport 1024:65535 --sport 53 -j ACCEPT iptables -A INPUT -p <udp/tcp> --dport 53 --sport 1024:65535 -j ACCEPT iptables -A OUTPUT -p <udp/tcp> --dport 53 --sport 1024:65535 -j ACCEPT iptables -A OUTPUT -p <udp/tcp> --dport 1024:65535 --sport 53 -j ACCEPT")
    run_command(container_dict["client"], "iptables -A INPUT -p udp --sport 67  -j ACCEPT iptables -A OUTPUT -p udp --dport 67 -j  ACCEPT")
    run_command(container_dict["client"], "iptables -A INPUT -p tcp --dport 80 -j ACCEPT iptables -A OUTPUT -p tcp --sport 80 -j ACCEPT")
    run_command(container_dict["client"], "iptables -A INPUT -p tcp --dport 443 -j ACCEPT iptables -A OUTPUT -p tcp --sport 443 -j ACCEPT")
    run_command(container_dict["client"], "iptables -P INPUT REJECT")
    run_command(container_dict["client"], "iptables -P OUTPUT REJECT")

    