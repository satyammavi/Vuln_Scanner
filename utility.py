import socket
import ipaddress

def find_local_ip():
    try:
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_socket.connect(("8.8.8.8", 80))
        local_ip = temp_socket.getsockname()[0]
        temp_socket.close()
        return local_ip
    except Exception as error:
        print(f"Error: {error}")
        return None

def find_subnet_range(ip):
    network_obj = ipaddress.ip_network(f"{ip}/24", strict=False)
    return network_obj

def ip_range(subnet):
    print(f"The IP range is {subnet.network_address} - {subnet.broadcast_address} ({len(list(subnet.hosts()))} hosts)")
