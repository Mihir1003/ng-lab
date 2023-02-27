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

# check installation of mitmproxy in testing
if [ $(execute_in_container testing mitmproxy --version) = "" ]; then
    echo "Mitmproxy is not installed in testing. Exiting"
    exit 1
fi

# write a mitm python script that intercepts "https://example.com/" and checks checks existence of string "Example Domain"
mitn_script = """
import mitmproxy.http
from mitmproxy import ctx

#check for string "Example Domain" in response
#success if string found in response and exit with failure if string not found
def check_string(flow: mitmproxy.http.HTTPFlow) -> None:
    if "Example Domain" in flow.response.text:
        ctx.log.info("String found in response")
        exit(0)
    else:
        ctx.log.info("String not found in response")
        exit(1)


#intercept response to "https://example.com/"
def response(flow: mitmproxy.http.HTTPFlow) -> None:
    if flow.request.pretty_url == "https://example.com/":
        ctx.log.info("Intercepted response to https://example.com/")
        check_string(flow)





"""
# write the above script to a file in testing
function write_mitm_script() {
    lxc exec testing -- bash -c "echo $mitn_script > mitm.py"
}

# write a shell function to execute the above script in testing
function execute_mitm_script() {
    lxc exec testing -- python3 mitm.py
}

# write a test to check if the above script is executed successfully
function test_mitm_script() {
    if [ $(execute_mitm_script) != "String found in response" ]; then
        echo "Mitm script failed. Exiting"
        exit 1
    fi
}





