import socket

def start_client(host='86.121.132.122', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to the server. Enter messages to send them. Type 'stop' to close the connection.")

    while True:
        message = input("What you want?\n")
        if (message == "speed"):
            client_socket.sendall(message.encode('utf-8'))
            data = client_socket.recv(1024)
            print(f"Server response:\n{data.decode('utf-8')}\n")

        if message == 'stop':
            client_socket.sendall(message.encode('utf-8'))
            client_socket.close()
            print("Connection closed.")
            break

if __name__ == "__main__":
    start_client()
