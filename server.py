import socket
import sys
import os
import pickle
import threading


BUFFER_SIZE = 1000
FORMAT = "utf-8"
HEADER_SIZE = 20
SERVER_IP = "127.0.0.1"
try: 
    SERVER_PORT = int(sys.argv[1])
except:
    print("\nrun the program like this:\n\npython server.py <port-number>")
    exit()


def put(connection, client_address):
    file_info = recv_obj(connection)

    with open(os.path.join(os.getcwd(), 'server_files', file_info['file_name']), 'wb') as file:
        file.write(file_info['file_data'])
    print(f"\nFile named {file_info['file_name']} successfully recieved from {client_address[0]}:{client_address[1]}")


def get(connection, client_address):
    response = {"isfile": True}
    file_name = connection.recv(BUFFER_SIZE).decode(FORMAT)
    file_path = os.path.join(os.getcwd(), 'server_files', file_name)
    if not os.path.isfile(file_path):
        response['isfile'] = False
        send_obj(connection, response)
        return

    with open(file_path, 'rb') as file:
        response['file_data'] = file.read()

    send_obj(connection, response)
    print(f"\nFile named {file_name} successfully sent to {client_address[0]}:{client_address[1]}")


def list_files(connection, client_address):
    mypath = os.path.join(os.getcwd(), 'server_files')
    server_files = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    send_obj(connection, server_files)
    print(f"\nLS command output sent successfully to {client_address[0]}:{client_address[1]}")


def send_obj(connection, obj):
    binary_data = pickle.dumps(obj)
    binary_data = f'{len(binary_data):<{HEADER_SIZE}}'.encode(FORMAT) + binary_data
    connection.sendall(binary_data)


def recv_obj(connection):
    full_binary_data = b''
    new_obj = True
    while True:
        binary_data = connection.recv(BUFFER_SIZE)
        if new_obj:
            msglen = int(binary_data[:HEADER_SIZE])
            new_obj = False

        full_binary_data += binary_data

        if len(full_binary_data)-HEADER_SIZE == msglen:
            return pickle.loads(full_binary_data[HEADER_SIZE:])


def threaded_client(connection, client_address):
    with connection:
        print(f"\n[NEW CONNECTION] {client_address[0]}:{client_address[1]} got connected.")
        while True:
            print("\n\nWaiting for instruction")
            data = connection.recv(BUFFER_SIZE).decode(FORMAT)
            print(f"\nRecieved instruction: {data}")

            match data:
                case "PUT" : put(connection, client_address)
                case "GET" : get(connection, client_address)
                case "LS" : list_files(connection, client_address)
                case "QUIT":
                    print(f"\n{client_address[0]}:{client_address[1]} successfully quited!")
                    break


print("\n[STARTING] Server is starting.")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)
    print(f"\n[LISTENING] Server is listening on {SERVER_IP}:{SERVER_PORT}")

    while True:
        connection, client_address = server_socket.accept()
        threading.Thread(target=threaded_client, args=(connection, client_address)).start()
