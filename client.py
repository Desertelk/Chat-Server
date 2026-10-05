import socket
import json
import threading

HOST = "127.0.0.1"
PORT = 50501

def send_json(message):
    data = json.dumps(message) + "\n"
    client_socket.sendall(data.encode())

def receive_messages():
    while True:
        data = server_file.readline()

        if not data: 
            print("Disconnected from server.")
            break

        message = json.loads(data)

        if message["type"] == "MESSAGE":
            print(f"\n{message['username']}: {message['message']}")
            print("> ", end="", flush=True)

        elif message["type"] == "PLAYER_LIST":
            print(f"\nConnected players: {', '.join(message['players'])}")
            print("> ", end="", flush=True)

        elif message["type"] == "SYSTEM":
            print(f"\n{message['message']}")
            print("> ", end="", flush=True)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))
server_file = client_socket.makefile("r", encoding="utf-8")

print(f"Connected to server at {HOST}:{PORT}")

username = input("Enter your username: ")

message = {
    "type": "JOIN",
    "username": username
}
send_json(message)

data = server_file.readline()
response = json.loads(data)
print(response["message"])


receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

while True:
    text = input("> ")

    if not text.strip():
        continue

    if text == "/players":
        message = {
            "type": "LIST_PLAYERS"
        }

        send_json(message)
        continue

    if text == "/exit":
        message = {
            "type": "EXIT"
        }

        send_json(message)
        break

    else:
        message = {
        "type": "MESSAGE",
        "username": username,
        "message": text
    }

    send_json(message)