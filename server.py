import socket
import json
import threading

HOST = "127.0.0.1"
PORT = 50501
clients = []



print(f"Server is listening on {HOST}:{PORT}")

def send_json(client_socket, message):
    data = json.dumps(message) + "\n"
    client_socket.sendall(data.encode())

def broadcast(message, sender_socket):
    print(f"Broadcasting: {message}")

    for client in clients:
        client_socket = client["socket"]

        if client_socket != sender_socket:
            try:
                send_json(client_socket, message)
                print(f"Sent to {client_socket.getpeername()}")
            except Exception as error:
                print(f"Broadcast Error: {error}")
            

def handle_client(client_socket, client_address):
    print(f"Client connected from {client_address}")

    client_file = client_socket.makefile("r", encoding="utf-8")
    data = client_file.readline()

    if not data:
        return

    # data = client_socket.recv(1024)
    message = json.loads(data)

    print(message)
    print(f"Request type: {message['type']}")
    print(f"Username: {message['username']}")
    
    clients.append({
        "username": message["username"],
        "socket": client_socket
        })

    response = {
        "status": "success",
        "message": f"{message['username']} joined the server."
    }

    send_json(client_socket, response)

    while True:
        # data = client_socket.recv(1024)
        data = client_file.readline()


        if not data:
            print(f"{message['username']} disconnected.")

            for client in clients:    
                if client["socket"] == client_socket:
                    clients.remove(client)
                    break

            client_socket.close()

        new_message = json.loads(data)
        print(new_message)
        if new_message["type"] == "MESSAGE":
            if new_message["message"].strip():
                broadcast(new_message, client_socket)

        elif new_message["type"] == "LIST_PLAYERS":
            player_names = []

            for client in clients:
                player_names.append(client["username"])

            response = {
                "type": "PLAYER_LIST",
                "players": player_names
            }

            send_json(client_socket, response)

        elif new_message["type"] == "EXIT":
            username = message['username']
            print(f"{username} left the server.")
            for client in clients:
                if client["socket"] == client_socket:
                    clients.remove(client)
                    break

            leave_message = {
                "type": "SYSTEM",
                "message": f"{username} has left chat."
            }

            broadcast(leave_message, client_socket)
            client_socket.close()
            break

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))
server_socket.listen()
print(f"Server is listening on {HOST}:{PORT}")

while True:
    client_socket, client_address = server_socket.accept()

    client_thread = threading.Thread(
        target=handle_client,
        args=(client_socket, client_address)
    )

    client_thread.start()