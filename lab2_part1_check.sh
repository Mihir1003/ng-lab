
router_ip = "192.168.22.101"
testing_ip_1 =  "192.168.22.102" 
testing_ip_2 =  "192.168.23.102" 
metasploitable_ip = "192.168.23.103" 
client_ip = "192.168.23.104" 

function check_internet() {
    ping -c 1 google.com > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "Connected to internet"
    else
        echo "Not connected to internet"
    fi
}


# write a shell function to check for connection for an ip address
function check_ip() {
    ping -c 1 $1 > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "Connection to $1 is up"
    else
        echo "Connection to $1 is down"
    fi
}



# function to execute 1 command in lxc container and return output
function execute_in_container() {
    lxc exec $1 -- $2
}

#convert the above pattern to a test function
function test_connection_router() {
    if [ $(execute_in_container router check_ip $1) = "Connection to $1 is down" ]; then
        echo "Router is not connected to $1. Exiting"
        exit 1
    fi
}

function test_no_connection_router() {
    if [ $(execute_in_container router check_ip $1) != "Connection to $1 is down" ]; then
        echo "Router is not connected to $1. Exiting"
        exit 1
    fi
}

# make similar function as above for testing, metasploitable and client
function test_connection_testing() {
    if [ $(execute_in_container testing check_ip $1) = "Connection to $1 is down" ]; then
        echo "Testing is not connected to $1. Exiting"
        exit 1
    fi
}

function test_connection_metasploitable() {
    if [ $(execute_in_container metasploitable check_ip $1) = "Connection to $1 is down" ]; then
        echo "Metasploitable is not connected to $1. Exiting"
        exit 1
    fi
}

function test_no_connection_metasploitable() {
    if [ $(execute_in_container metasploitable check_ip $1) != "Connection to $1 is down" ]; then
        echo "Metasploitable is not connected to $1. Exiting"
        exit 1
    fi
}

function test_connection_client() {
    if [ $(execute_in_container client check_ip $1) = "Connection to $1 is down" ]; then
        echo "Client is not connected to $1. Exiting"
        exit 1
    fi
}

function test_no_connection_client() {
    if [ $(execute_in_container client check_ip $1) != "Connection to $1 is down" ]; then
        echo "Client is not connected to $1. Exiting"
        exit 1
    fi
}

#test if container can access internet
function container_access_to_internet {
    if [ $(execute_in_container $1 check_internet) != "Connected to internet" ]; then
        echo "Container $1 is not connected to internet. Exiting"
        exit 1
    fi
}
#test if container cannot access internet
function container_no_access_to_internet {
    if [ $(execute_in_container $1 check_internet) != "Connected to internet" ]; then
        echo "Container $1 is connected to internet. Exiting"
        exit 1
    fi
}

# function to check if conatiner has ip address
function container_has_ip {
    if [ $(execute_in_container $1 ip a | grep $2) = "" ]; then
        echo "Container $1 does not have ip address $2. Exiting"
        exit 1
    fi
}

# client and metasplopitable should be able to connect to everything
test_connection_client  $router_ip
test_connection_client  $testing_ip_1
test_connection_client  $testing_ip_2
test_connection_client  $metasploitable_ip

test_connection_metasploitable  $router_ip
test_connection_metasploitable  $testing_ip_1
test_connection_metasploitable  $testing_ip_2
test_connection_metasploitable  $client_ip

# client and metasploiatble should be able to connect to internet
container_access_to_internet client
container_access_to_internet metasploitable

# test if client is able to use ICMP
if [ $(execute_in_container client ping -c 1 $testing_ip_1) != "1 packets transmitted, 1 received, 0% packet loss, time 0ms" ]; then
    echo "Client is not able to use ICMP. Exiting"
    exit 1
fi

# test if client is able to use HTTP and HTTPS
if [ $(execute_in_container client curl -s -o /dev/null -w "%{http_code}" http://google.com) != "200" ]; then
    echo "Client is not able to use HTTP. Exiting"
    exit 1
fi

# test if client is able to use  HTTPS
if [ $(execute_in_container client curl -s -o /dev/null -w "%{http_code}" https://google.com) != "200" ]; then
    echo "Client is not able to use HTTPS. Exiting"
    exit 1
fi


# test if client is able to use  DHCP
if [ $(execute_in_container client dhclient -v) != "Internet Systems Consortium DHCP Client 4.3.5" ]; then
    echo "Client is not able to use DHCP. Exiting"
    exit 1
fi

# test if client is able to use  DNS
if [ $(execute_in_container client dig google.com) != ";; ANSWER SECTION:" ]; then
    echo "Client is not able to use DNS. Exiting"
    exit 1
fi

# test if client is able to use  NTP
if [ $(execute_in_container client ntpq -p) != "remote refid st t when poll reach delay offset jitter" ]; then
    echo "Client is not able to use NTP. Exiting"
    exit 1
fi

# test if client is able to use  SSH
if [ $(execute_in_container client ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -i /root/.ssh/id_rsa root@$testing_ip_1 "echo 'SSH is working'") != "SSH is working" ]; then
    echo "Client is not able to use SSH. Exiting"
    exit 1
fi

#test client cannot use ftp
if [ $(execute_in_container client ftp $testing_ip_1) != "Connected to $testing_ip_1." ]; then
    echo "Client is able to use FTP. Exiting"
    exit 1
fi

#test client cannot use telnet
if [ $(execute_in_container client telnet $testing_ip_1) != "Trying $testing_ip_1..." ]; then
    echo "Client is able to use telnet. Exiting"
    exit 1
fi

#test client cannot use smtp
if [ $(execute_in_container client telnet $testing_ip_1 25) != "Trying $testing_ip_1..." ]; then
    echo "Client is able to use smtp. Exiting"
    exit 1
fi

#test client cannot use pop3
if [ $(execute_in_container client telnet $testing_ip_1 110) != "Trying $testing_ip_1..." ]; then
    echo "Client is able to use pop3. Exiting"
    exit 1
fi

#test client blocks all traffic from metasploitable
test_connection_metasploitable $client_ip

#write a function to start a python webserver in a container
function start_webserver {
    execute_in_container $1 python -m SimpleHTTPServer 80 &
}

#start webserver in client
start_webserver client

#test if client has blocked http by checking http connection to client webserver via metasploitable
if [ $(execute_in_container metasploitable curl -s -o /dev/null -w "%{http_code}" http://$client_ip) != "200" ]; then
    echo "Client is not blocking HTTP. Exiting"
    exit 1
fi

#test if client has not blocked https by checking https connection to client webserver via metasploitable
if [ $(execute_in_container metasploitable curl -s -o /dev/null -w "%{http_code}" https://$client_ip) != "200" ]; then
    echo "Client is blocking HTTPS. Exiting"
    exit 1
fi

#test if metasploitable can connect to client
test_connection_metasploitable $client_ip





#


