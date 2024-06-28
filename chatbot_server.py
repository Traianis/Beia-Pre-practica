import socket
import json

def start_server(host='0.0.0.0', port=12345):
    # TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"The server has started and is listening on {host}:{port}")

    try:
        # Waiting for connection
        client_socket, client_address = server_socket.accept()
        print(f"Connected to {client_address}\n")

        while True:
            # Receiving data
            data = client_socket.recv(1024)
            if data:
                data_decoded = data.decode('utf-8')
                print(f"Received: {data_decoded}")
                if data_decoded == "stop":
                    # Connection close
                    client_socket.close()
                    server_socket.close()
                    break
                if data_decoded == "speed":
                    with open("/home/student/Desktop/BEIA/speed_data.txt", 'r') as file:
                        lines = file.readlines()
                        if lines:
                            last_line = lines[-1].strip()
                        else:
                            # Connection close
                            client_socket.close()
                            server_socket.close()
                            break
                    last_data = json.loads(last_line)
                    speed = str(last_data.get("speed"))
                    # Send the data
                    client_socket.sendall(f"The current speed is {speed}\n".encode('utf-8'))
                
            else:
                print(f"Client {client_address} disconnected\n")
                client_socket.close()
                try:
                    client_socket, client_address = server_socket.accept()
                except KeyboardInterrupt:
                    print("Server closed!\n")
                    server_socket.close()
    finally:
        print("Closing the server and the socket.")
        client_socket.close()
        server_socket.close()
            

if __name__ == "__main__":
    start_server()
