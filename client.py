import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Received: {message}")
        except ConnectionResetError:
            break
    client_socket.close()

def send_messages(client_socket):
    while True:
        try:
            message = input("Enter message: ")
            client_socket.send(message.encode('utf-8'))
        except EOFError:
            print("Input stream has been closed.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('localhost', 12346))
        print("Connected to server.")

        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()

        send_thread = threading.Thread(target=send_messages, args=(client_socket,))
        send_thread.start()

    except ConnectionRefusedError:
        print("Connection refused. Make sure the server is running.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    connect_to_server()
