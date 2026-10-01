import socket
import json

HOST = "127.0.0.1"
PORT = 50501

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))

print(f"Connected to server at {HOST}:{PORT}")

username = input("Enter your username: ")

message = {
    "type": "JOIN",
    "username": username
}
client_socket.send(json.dumps(message).encode())

data = client_socket.recv(1024)
response = json.loads(data.decode())
print(response["message"])

while True:
    text = input("> ")

    message = {
        "type": "MESSAGE",
        "username": username,
        "message": text
    }

    client_socket.send(json.dumps(message).encode())