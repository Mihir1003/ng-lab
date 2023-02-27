router_ip="192.168.22.101"
testing_ip_1="192.168.22.102" 
testing_ip_2="192.168.23.102" 
metasploitable_ip="192.168.23.103" 
client_ip="192.168.23.104" 

check_internet() {
    ping -c 1 google.com > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "Connected to internet"
    else
        echo "Not connected to internet"
    fi
}


# write a shell function to check for connection for an ip address
check_ip() {
    ping -c 1 $1 > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "Connection to $1 is up"
    else
        echo "Connection to $1 is down"
    fi
}



# function to execute 1 command in lxc container and return output
execute_in_container() {
    lxc exec $1 -- $2
}

#convert the above pattern to a test function
test_connection_router() {
    if [ $(execute_in_container router check_ip $1) = "Connection to $1 is down" ]; then
        echo "Router is not connected to $1. Exiting"
        exit 1
    fi
}

test_no_connection_router() {
    if [ $(execute_in_container router check_ip $1) != "Connection to $1 is down" ]; then
        echo "Router is not connected to $1. Exiting"
        exit 1
    fi
}

# make similar function as above for testing, metasploitable and client
test_connection_testing() {
    if [ $(execute_in_container testing check_ip $1) = "Connection to $1 is down" ]; then
        echo "Testing is not connected to $1. Exiting"
        exit 1
    fi
}

test_connection_metasploitable() {
    if [ $(execute_in_container metasploitable check_ip $1) = "Connection to $1 is down" ]; then
        echo "Metasploitable is not connected to $1. Exiting"
        exit 1
    fi
}

test_no_connection_metasploitable() {
    if [ $(execute_in_container metasploitable check_ip $1) != "Connection to $1 is down" ]; then
        echo "Metasploitable is not connected to $1. Exiting"
        exit 1
    fi
}

test_connection_client() {
    if [ $(execute_in_container client check_ip $1) = "Connection to $1 is down" ]; then
        echo "Client is not connected to $1. Exiting"
        exit 1
    fi
}

test_no_connection_client() {
    if [ $(execute_in_container client check_ip $1) != "Connection to $1 is down" ]; then
        echo "Client is not connected to $1. Exiting"
        exit 1
    fi
}

#test if container can access internet
container_access_to_internet() {
    if [ $(execute_in_container $1 check_internet) != "Connected to internet" ]; then
        echo "Container $1 is not connected to internet. Exiting"
        exit 1
    fi
}
#test if container cannot access internet
container_no_access_to_internet() {
    if [ $(execute_in_container $1 check_internet) != "Connected to internet" ]; then
        echo "Container $1 is connected to internet. Exiting"
        exit 1
    fi
}

# function to check if conatiner has ip address
container_has_ip() {
    if lxc exec "$1" --  "ip a | grep $2" == "" ; then
        echo "Container $1 does not have ip address $2. Exiting"
        exit 1
    fi
}

container_has_ip router $router_ip
container_has_ip testing $testing_ip_1
container_has_ip testing $testing_ip_2
container_has_ip metasploitable $metasploitable_ip
container_has_ip client $client_ip

echo "IP addresses correctly configured"


# #only router can access internet
# container_access_to_internet router
# #rest cannot access internet
# container_no_access_to_internet testing
# container_no_access_to_internet metasploitable
# container_no_access_to_internet client


# echo "Internet Access correctly configured"




# # write test cases to check router connection to testing, metasploitable and client
# test_connection_router $testing_ip_1
# test_connection_router $testing_ip_2
# test_no_connection_router $metasploitable_ip
# test_no_connection_router $client_ip

# echo "Router correctly configured"

# #testing can access metasploitable and client and router
# test_connection_testing $metasploitable_ip
# test_connection_testing $client_ip
# test_connection_testing $router_ip

# echo "Testing correctly configured"

# # client can access testing and metasploitable but not router
# test_connection_client $testing_ip_1
# test_connection_client $testing_ip_2
# test_connection_client $metasploitable_ip
# test_no_connection_client $router_ip

# echo "Client correctly configured"

# # metasploitable can access testing and client but not router
# test_connection_metasploitable $testing_ip_1
# test_connection_metasploitable $testing_ip_2
# test_connection_metasploitable $client_ip
# test_no_connection_metasploitable $router_ip

# echo "Metasploitable correctly configured"


# write a functui