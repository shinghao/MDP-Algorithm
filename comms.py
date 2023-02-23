import socket

# Define the address and port to listen on
host = ''     # Listen on all available interfaces
port = 12345  # Choose a port number

# Create a TCP/IP socket and bind it to the address and port
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))

# Listen for incoming connections
sock.listen(1)
print(f'Listening on {host}:{port}...')

# Wait for a connection
conn, addr = sock.accept()
print(f'Connected by {addr}')

while True:
    # Receive data from the client
    data = conn.recv(1024)
    if not data:
        break
    message = data.decode()
    print(f'Received "{message}" from {addr}')

    # Send a response to the client
    response = f'You said "{message}"'
    conn.sendall(response.encode())

# Clean up the connection
conn.close()
sock.close()