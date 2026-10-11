import socket
import json
import threading

# Server connection settings
HOST = "127.0.0.1"
PORT = 12345

# Converts python dictionary to JSON and sends it to the server.
def send_json(message):
    # Adds a newline so the server can identify complete messages.
    data = json.dumps(message) + "\n"
    client_socket.sendall(data.encode())

# Continuously listens for responses and messages from the server.
def receive_messages():
    while True:
        # Read one complete JSON message from the server.
        data = server_file.readline()

        # An empty read means the server closed the connection.
        if not data: 
            print("Disconnected from server.")
            break

        # Converts the received JSON to a python library
        message = json.loads(data)

        # Display chat messages from ther connected users.
        if message["type"] == "MESSAGE":
            print(f"\n{message['username']}: {message['message']}")
            print("> ", end="", flush=True)

        # Display the usernames returned by the server
        elif message["type"] == "PLAYER_LIST":
            print(f"\nConnected players: {', '.join(message['players'])}")
            print("> ", end="", flush=True)

        # Display server notifications, such as users leaving.
        elif message["type"] == "SYSTEM":
            print(f"\n{message['message']}")
            print("> ", end="", flush=True)

# Create an IPv4 TCP socket and connect to the server 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))

# Use readline() to receive newline-delimited JSON messages.
server_file = client_socket.makefile("r", encoding="utf-8")

print(f"Connected to server at {HOST}:{PORT}")

# Asks for a username before entering the chat.
username = input("Enter your username: ")

# Sends a JOIN request to register the username with the server.
message = {
    "type": "JOIN",
    "username": username
}
send_json(message)

# Wait for the server to confirm the user joined successfully.
data = server_file.readline()
response = json.loads(data)
print(response["message"])

# Start a separate thread to receive incoming messages.
# This allows the client to receive messages while waiting for user input.
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Keep accepting commands and chat messages from the user.
while True:
    text = input("> ")

    # Ignore messages containing only whitespace
    if not text.strip():
        continue

    # Request the list of currently connected users.
    if text == "/players":
        message = {
            "type": "LIST_PLAYERS"
        }

        send_json(message)
        continue

    # Tell the server this user is leaving the chat
    if text == "/exit":
        message = {
            "type": "EXIT"
        }

        send_json(message)
        break

    # Treat any other input as a chat message.
    else:
        message = {
        "type": "MESSAGE",
        "username": username,
        "message": text
    }

    # Send the chat message to the server for broadcasting.
    send_json(message)