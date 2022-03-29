# FTP Implementation with Socket Programming

A simple File Transfer Protocol project using Socket Programming in Python implemented by Ali Safinal.

On the client side, there is a Graphic User Interface that provide these functions:
- `ls`: Show List of server files
- `get <file-name>`: Download `<file-name>` file from the server
- `put <file-name>`: Upload `<file-name>` file to the server 
- `quit`: Exit the client program

## Requirements
- Python version `3.10.0` or higher.
- PyQt5 version `5.15.6`.
## How to Run
0. Install the requirements
    1. Open a Command Prompt/Terminal and change the working directory to the project directory (**don't skip this step**):
        ```bash
        cd ftp-implementation
        ```
    2. Enter the following command:
        ```bash
        pip install -r requirements.txt
        ```
1. Run the server
    1. Open a Command Prompt/Terminal and change the working directory to the project directory (**don't skip this step**):
        ```bash
        cd ftp-implementation
        ```
    2. Enter the following command to run the server:
        ```bash
        # python server.py <port-number>
        python server.py 12345
        ```
2. Run a client
    1. Open another Command Prompt/Terminal and change the working directory to the project directory (**don't skip this step**):
        ```bash
        cd ftp-implementation
        ```
    2. Enter the following command to run a client:
        ```bash
        # python client.py 127.0.0.1 <port-number>
        python client.py 127.0.0.1 12345
        ```
3. **(Optional)** You can repeat step 2 as many times as you want! **This project supports multi-clients feature.**

Here is an example photo showing how does the program look like:

![example photo](https://s6.uupload.ir/files/gui_iqf0.png)
