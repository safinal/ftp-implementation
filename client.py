import socket
import sys
import os
import pickle


# SERVER_IP = sys.argv[1] 
# SERVER_PORT = int(sys.argv[2])
SERVER_IP = 'localhost'
SERVER_PORT = 12345
BUFFER_SIZE = 1000
FORMAT = "utf-8"
HEADER_SIZE = 10


def connect_to_server() -> bool:
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print("Connection sucessful")
        return True
    except:
        print("Connection unsucessful. Make sure the server is online.")
        return False


def put(file_name: str):
    file_path = os.path.join(os.getcwd(), 'client_files', file_name)
    if not os.path.isfile(file_path):
        print(f'\nYou do not have a file named "{file_name}" to upload on the server')
        return
    client_socket.send("PUT".encode(FORMAT))
    client_socket.send(file_name.encode(FORMAT))
    with open(file_path, 'rb') as file:   
        send_obj(file.read())    


def get(file_name: str):
    client_socket.send("GET".encode(FORMAT))

    client_socket.send(file_name.encode(FORMAT))

    response = recv_obj()
    if not response['isfile']:
        print(f"\nThere is no file on the server with this name: {file_name}")
        return

    with open(os.path.join(os.getcwd(), 'client_files', file_name), 'wb') as file:
        file.write(response['file_data'])


def list_files():
    client_socket.send("LS".encode(FORMAT))

    server_files = recv_obj()
    print("\nList of server files:")
    print(*server_files, sep='\n', end='\n\n')


def _quit():
    client_socket.send("QUIT".encode(FORMAT))
    exit()

def send_obj(obj):
    binary_data = pickle.dumps(obj)
    binary_data = f'{len(binary_data):<{HEADER_SIZE}}'.encode(FORMAT) + binary_data
    client_socket.send(binary_data)

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


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
is_connected = connect_to_server()
if not is_connected : exit()

while True:
    prompt = input("\nFTP> ").strip().split()
    
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
            _quit()
        case _ : print("Command not recognised; please try again")
