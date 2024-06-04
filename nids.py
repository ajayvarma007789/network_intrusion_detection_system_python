import socket
import threading
import subprocess
# Define constants
HOST = '127.0.1.1' # Use your server's IP address here
PORT = 80
MAX_CONNECTIONS = 100
BLOCK_THRESHOLD = 50 # Adjust as needed
BLOCK_DURATION = 60 # Block duration in seconds




# Dictionary to store the count of connections per IP address
connections_count = {}




# Function to handle client connections
def handle_connection(client_socket, addr):
    global connections_count
    ip = addr[0]
    if ip not in connections_count:
        connections_count[ip] = 1
    else:
        connections_count[ip] += 1

    if connections_count[ip] > BLOCK_THRESHOLD:
        print(f"Blocking {ip} for {BLOCK_DURATION} seconds")
        block_ip(ip)

    client_socket.close()

# Function to block an IP address using firewall rules
def block_ip(ip):
# Example command for iptables on Linux
#subprocess.run(['iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP'])
# Example command for Windows Firewall
    subprocess.run(['netsh', 'advfirewall', 'firewall', 'add', 'rule', 'name="Block ' + ip + '"', 'dir=in', 'action=block', 'remoteip=' + ip])

# Function to listen for incoming connections
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(MAX_CONNECTIONS)
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Received connection from {addr[0]}:{addr[1]}")
        client_thread = threading.Thread(target=handle_connection, args=(client_socket, addr))
        client_thread.start()
# Start the server
start_server()
