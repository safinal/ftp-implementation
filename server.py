import socket
import sys
import os
import pickle
from _thread import start_new_thread


SERVER_IP = "127.0.0.1"
# SERVER_PORT = int(sys.argv[1])
SERVER_PORT = 12345
BUFFER_SIZE = 1000
FORMAT = "utf-8"
HEADER_SIZE = 10


def put():
    file_info = recv_obj()

    with open(os.path.join(os.getcwd(), 'server_files', file_info['file_name']), 'wb') as file:
        file.write(file_info['file_data'])
    print(f"\nFile named {file_info['file_name']} successfully recieved from the client!")


def get():
    response = {"isfile": True}
    file_name = connection.recv(BUFFER_SIZE).decode(FORMAT)
    file_path = os.path.join(os.getcwd(), 'server_files', file_name)
    if not os.path.isfile(file_path):
        response['isfile'] = False
        send_obj(response)
        return

    with open(file_path, 'rb') as file:
        response['file_data'] = file.read()

    send_obj(response)
    print(f"\nFile named {file_name} successfully sent to the client!")


def list_files():
    mypath = os.path.join(os.getcwd(), 'server_files')
    server_files = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    send_obj(server_files)
    print("\nLS command output sent successfully!")


def send_obj(obj):
    binary_data = pickle.dumps(obj)
    binary_data = f'{len(binary_data):<{HEADER_SIZE}}'.encode(FORMAT) + binary_data
    connection.sendall(binary_data)


def recv_obj():
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


print("\n[STARTING] Server is starting.")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)
    print(f"\n[LISTENING] Server is listening on {SERVER_IP}:{SERVER_PORT}")

    connection, client_address = server_socket.accept()
    print(f"\n[NEW CONNECTION] {client_address[0]}:{client_address[1]} got connected.")
    while True:
        print("\n\nWaiting for instruction")
        data = connection.recv(BUFFER_SIZE).decode(FORMAT)
        print(f"\nRecieved instruction: {data}")

        match data:
            case "PUT" : put()
            case "GET" : get()
            case "LS" : list_files()
            case "QUIT": exit()
