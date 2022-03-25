import socket
import sys
import os
import pickle


BUFFER_SIZE = 1000
FORMAT = "utf-8"
HEADER_SIZE = 20
try:
    SERVER_IP = sys.argv[1] 
    SERVER_PORT = int(sys.argv[2])
except:
    print("\nrun the program like this:\n\npython client.py 127.0.0.1 <port-number>")
    exit()


def connect_to_server() -> bool:
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print("Connection sucessful")
        return True
    except:
        print("Connection unsucessful. Make sure the server is online.")
        return False


def put(file_name: str):
    client_dir_path = os.path.join(os.getcwd(), f'{client_socket.getsockname()[0]}, {client_socket.getsockname()[1]}')
    if not os.path.isdir(client_dir_path):
        os.mkdir(client_dir_path)
    file_path = os.path.join(client_dir_path, file_name)
    if not os.path.isfile(file_path):
        print(f'\nYou do not have a file named "{file_name}" to upload on the server')
        return
    client_socket.sendall("PUT".encode(FORMAT))
    file_info = {"file_name": file_name}
    with open(file_path, 'rb') as file:   
        file_info["file_data"] = file.read()
    send_obj(file_info)


def get(file_name: str):
    client_socket.sendall("GET".encode(FORMAT))

    client_socket.sendall(file_name.encode(FORMAT))

    response = recv_obj()
    if not response['isfile']:
        print(f"\nThere is no file on the server with this name: {file_name}")
        return
    client_dir_path = os.path.join(os.getcwd(), f'{client_socket.getsockname()[0]}, {client_socket.getsockname()[1]}')
    if not os.path.isdir(client_dir_path):
        os.mkdir(client_dir_path)

    with open(os.path.join(client_dir_path, file_name), 'wb') as file:
        file.write(response['file_data'])


def list_files():
    client_socket.sendall("LS".encode(FORMAT))

    server_files = recv_obj()
    print("\nList of server files:")
    print(*server_files, sep='\n', end='\n\n')


def send_obj(obj):
    binary_data = pickle.dumps(obj)
    binary_data = f'{len(binary_data):<{HEADER_SIZE}}'.encode(FORMAT) + binary_data
    client_socket.sendall(binary_data)


def recv_obj():
    full_binary_data = b''
    new_obj = True
    while True:
        binary_data = client_socket.recv(BUFFER_SIZE)
        if new_obj:
            msglen = int(binary_data[:HEADER_SIZE])
            new_obj = False

        full_binary_data += binary_data

        if len(full_binary_data)-HEADER_SIZE == msglen:
            return pickle.loads(full_binary_data[HEADER_SIZE:])


print("""

Call one of the following functions:
PUT file_name  : Upload a file to server
LS             : List of server files
GET file_name  : Download a file from server
QUIT           : Exit
""")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    is_connected = connect_to_server()
    if not is_connected : exit()

    while True:
        prompt = input("\nFTP> ").strip().split()
        if len(prompt) == 0 : prompt.append('')

        match prompt[0].upper():
            case "PUT":
                if len(prompt) != 2:
                    print('You must pass only 1 parameter to this function!')
                    continue
                put(prompt[1])
            case "GET":
                if len(prompt) != 2:
                    print('You must pass only 1 parameter to this function!')
                    continue            
                get(prompt[1])
            case "LS":
                if len(prompt) != 1:
                    print('This function does not accept any paramters!')
                    continue              
                list_files()
            case "QUIT":
                if len(prompt) != 1:
                    print('This function does not accept any paramters!')
                    continue           
                client_socket.sendall("QUIT".encode(FORMAT))
                break
            case _ : print("Command not recognised; please try again")
