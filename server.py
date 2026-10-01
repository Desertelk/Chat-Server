import socket
import json
import threading

HOST = "127.0.0.1"
PORT = 50501
clients = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Server is listening on {HOST}:{PORT}")

def broadcast(message):
    for client in clients:
        client.send(json.dumps(message).encode())

def handle_client(client_socket, client_address):
    print(f"Client connected from {client_address}")

    data = client_socket.recv(1024)
    message = json.loads(data.decode())

    print(message)
    print(f"Request type: {message['type']}")
    print(f"Username: {message['username']}")
    
    clients.append(client_socket)

    response = {
        "status": "success",
        "message": f"{message['username']} joined the server."
    }

    client_socket.send(json.dumps(response).encode())

    while True:
        data = client_socket.recv(1024)

        if not data:
            print(f"{message['username']} disconnected.")
            clients.remove(client_socket)
            client_socket.close()
            break

        new_message = json.loads(data.decode())
        print(new_message)
        if new_message["type"] == "MESSAGE":
            broadcast(new_message)


while True:
    client_socket, client_address = server_socket.accept()

    client_thread = threading.Thread(
        target=handle_client,
        args=(client_socket, client_address)
    )

    client_thread.start()



