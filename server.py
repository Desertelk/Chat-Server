import socket
import json
import threading

# Server configuration
# Localhost allows clients on the same computer to connect.
HOST = "127.0.0.1"
PORT = 12345

# Stores each connected user's username and socket
clients = []



print(f"Server is listening on {HOST}:{PORT}")

# Convert a dictionary to JSON and send it over TCP.
def send_json(client_socket, message):
    # Newline separates messages because TCP is a byte stream.
    data = json.dumps(message) + "\n"
    client_socket.sendall(data.encode())

# Send a message to every connected client except the sender.
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
            
# Handle requests from one connected client.
def handle_client(client_socket, client_address):
    print(f"Client connected from {client_address}")

    # Read complete newline-delimited JSON messages.
    client_file = client_socket.makefile("r", encoding="utf-8")
    data = client_file.readline()

    if not data:
        return

    #  The first request registers the user's username.
    message = json.loads(data)

    print(message)
    print(f"Request type: {message['type']}")
    print(f"Username: {message['username']}")

    # Associate the username with the connection.
    clients.append({
        "username": message["username"],
        "socket": client_socket
        })

    # Confirm that the user joined successfully
    response = {
        "status": "success",
        "message": f"{message['username']} joined the server."
    }

    send_json(client_socket, response)

    # Keep listening for requests until the user disconnects.
    while True:
        data = client_file.readline()

        # An empty read means the connection was closed.
        if not data:
            print(f"{message['username']} disconnected.")

            for client in clients:    
                if client["socket"] == client_socket:
                    clients.remove(client)
                    break

            client_socket.close()

        # Conver the received json into a python dictionary.
        new_message = json.loads(data)
        print(new_message)

        if new_message["type"] == "MESSAGE":
            # Ignore empty messages and broadcast valid ones.
            if new_message["message"].strip():
                broadcast(new_message, client_socket)

        elif new_message["type"] == "LIST_PLAYERS":
            # Collect usernames and return them to the requester.
            player_names = []

            for client in clients:
                player_names.append(client["username"])

            response = {
                "type": "PLAYER_LIST",
                "players": player_names
            }

            send_json(client_socket, response)

        elif new_message["type"] == "EXIT":
            # Remove the departing user from the player list
            username = message['username']
            print(f"{username} left the server.")
            for client in clients:
                if client["socket"] == client_socket:
                    clients.remove(client)
                    break

            # Notify all remaining users about the departure
            leave_message = {
                "type": "SYSTEM",
                "message": f"{username} has left chat."
            }

            broadcast(leave_message, client_socket)
            client_socket.close()
            break

# Create an IPv4 TCP socket and start listening.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))
server_socket.listen()
print(f"Server is listening on {HOST}:{PORT}")

# Accept new clients and give each a separate thread.
# This allows multiple users to communicate simultaneously
while True:
    client_socket, client_address = server_socket.accept()

    client_thread = threading.Thread(
        target=handle_client,
        args=(client_socket, client_address)
    )

    client_thread.start()