# TCP Chat Server

## Overview

This project is a Python-based TCP client-server chat application that allows multiple users to connect to a server and communicate in real time.

The purpose of this project was to learn more about network programming, TCP sockets, client-server communication, multithreading, and JSON-based messaging. I wanted to understand how multiple programs communicate over a network and how a server can process different requests from connected clients.

## Software Demo Video

[Software Demonstration Video](https://youtu.be/4ALw0LdB5lA)

In this video, I demonstrate starting the server, connecting multiple clients, sending messages, listing connected players, and disconnecting users.

## Development Environment

The following tools and technologies were used to develop this project:

- **Visual Studio Code:** Code editor used to write and test the application.
- **Python 3:** Programming language used to develop the client and server.
- **Socket Library:** Used to establish TCP connections and exchange data.
- **Threading Library:** Used to support multiple simultaneous clients.
- **JSON Library:** Used to format requests and responses exchanged over the network.

All three Python libraries are built into Python, so no additional third-party packages are required.

## Features

The chat application supports four different request types:

1. **JOIN:** Registers a username when a client connects to the server.
2. **MESSAGE:** Sends a message to the server, which broadcasts it to other connected users.
3. **LIST_PLAYERS:** Allows users to type `/players` to request a list of currently connected users.
4. **EXIT:** Allows users to type `/exit` to disconnect from the server.

When a user exits, the server also sends a system notification to the remaining connected users.

The server uses separate threads to manage multiple clients simultaneously. Messages are transmitted using JSON, with newline characters separating individual messages.

## How to Run the Program

1. Make sure Python 3 is installed on your computer.
2. Open the project folder in Visual Studio Code or a terminal.
3. Start the server by running:

   ```bash
   python server.py
   ```

4. Open a separate terminal and start a client:

   ```bash
   python client.py
   ```

5. Enter a username when prompted.
6. Open additional terminals and run `python client.py` to connect more users.
7. Type messages to communicate with other connected users.

### Available Commands

| Command | Description |
|---------|-------------|
| Regular text | Sends a chat message to other connected users |
| `/players` | Displays the currently connected usernames |
| `/exit` | Disconnects from the server |

**Note:** The application currently uses `127.0.0.1` (localhost) and port `50501`, so the server and clients are intended to run on the same computer.

## Useful Websites

The following resources provide information about the networking concepts and Python libraries used in this project:

- [Python Socket Programming Documentation](https://docs.python.org/3/library/socket.html)
- [Python Threading Documentation](https://docs.python.org/3/library/threading.html)
- [Python JSON Documentation](https://docs.python.org/3/library/json.html)
- [Python Socket Programming HOWTO](https://docs.python.org/3/howto/sockets.html)

## Future Work

Some improvements I would like to make include:

- Add notifications when new users join the server.
- Improve terminal formatting so incoming messages do not interrupt the user's typing.
- Add private messaging between users.
- Improve error handling for unexpected disconnections.
- Support connections from other computers on the same network.