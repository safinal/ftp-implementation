import socket
import sys
import os
import pickle
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDir


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


def put(ui, file_name: str):
    file_path = os.path.join(client_dir_path, file_name)
    if not os.path.isfile(file_path):
        ui.output_txt.setPlainText(f'\nYou do not have a file named "{file_name}" to upload on the server')
        return
    client_socket.sendall("PUT".encode(FORMAT))
    file_info = {"file_name": file_name}
    with open(file_path, 'rb') as file:   
        file_info["file_data"] = file.read()
    send_obj(file_info)


def get(ui, file_name: str):
    client_socket.sendall("GET".encode(FORMAT))

    client_socket.sendall(file_name.encode(FORMAT))

    response = recv_obj()
    if not response['isfile']:
        ui.output_txt.setPlainText(f"\nThere is no file on the server with this name: {file_name}")
        return

    with open(os.path.join(client_dir_path, file_name), 'wb') as file:
        file.write(response['file_data'])


def list_files(ui):
    client_socket.sendall("LS".encode(FORMAT))

    server_files = recv_obj()
    ui.output_txt.setPlainText("\nList of server files:")
    ui.output_txt.setPlainText('\n'.join(server_files) + '\n\n')


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


class Main(QtWidgets.QTreeView):
    def __init__(self, centralwidget):
        QtWidgets.QTreeView.__init__(self, centralwidget)
        model = QtWidgets.QFileSystemModel()
        self.setModel(model)
        model.setRootPath(QDir.rootPath())
        self.setRootIndex(model.index(client_dir_path))
        self.doubleClicked.connect(self.test)

    def test(self):
        pass


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(790, 476)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(590, 290, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.par_txtbox = QtWidgets.QTextEdit(self.centralwidget)
        self.par_txtbox.setEnabled(True)
        self.par_txtbox.setGeometry(QtCore.QRect(590, 370, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.par_txtbox.setFont(font)
        self.par_txtbox.setObjectName("par_txtbox")
        self.send_button = QtWidgets.QPushButton(self.centralwidget)
        self.send_button.setGeometry(QtCore.QRect(590, 420, 51, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.send_button.setFont(font)
        self.send_button.setAutoFillBackground(False)
        self.send_button.setObjectName("send_button")
        self.client_dir_trv = Main(self.centralwidget)
        self.client_dir_trv.setGeometry(QtCore.QRect(20, 10, 751, 231))
        self.client_dir_trv.setObjectName("client_dir_trv")
        self.command_label = QtWidgets.QLabel(self.centralwidget)
        self.command_label.setGeometry(QtCore.QRect(590, 250, 71, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.command_label.setFont(font)
        self.command_label.setObjectName("command_label")
        self.quit_button = QtWidgets.QPushButton(self.centralwidget)
        self.quit_button.setGeometry(QtCore.QRect(720, 420, 51, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.quit_button.setFont(font)
        self.quit_button.setObjectName("quit_button")
        self.par_label = QtWidgets.QLabel(self.centralwidget)
        self.par_label.setGeometry(QtCore.QRect(590, 340, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.par_label.setFont(font)
        self.par_label.setObjectName("par_label")
        self.output_txt = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.output_txt.setEnabled(True)
        self.output_txt.setGeometry(QtCore.QRect(20, 260, 551, 191))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.output_txt.setFont(font)
        self.output_txt.setReadOnly(True)
        self.output_txt.setPlainText("")
        self.output_txt.setObjectName("output_txt")
        self.help_button = QtWidgets.QPushButton(self.centralwidget)
        self.help_button.setGeometry(QtCore.QRect(660, 420, 51, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.help_button.setFont(font)
        self.help_button.setAutoFillBackground(False)
        self.help_button.setObjectName("help_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.help_button.clicked.connect(self.show_popup)
        self.quit_button.clicked.connect(self.quit_pressed)
        self.send_button.clicked.connect(self.send_pressed)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.comboBox.setItemText(0, _translate("MainWindow", "LS"))
        self.comboBox.setItemText(1, _translate("MainWindow", "GET"))
        self.comboBox.setItemText(2, _translate("MainWindow", "PUT"))
        self.par_txtbox.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Segoe UI\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.send_button.setText(_translate("MainWindow", "SEND"))
        self.command_label.setText(_translate("MainWindow", "Command"))
        self.quit_button.setText(_translate("MainWindow", "QUIT"))
        self.par_label.setText(_translate("MainWindow", "Parameter"))
        self.help_button.setText(_translate("MainWindow", "HELP"))
        

    def send_pressed(self):
        command = self.comboBox.currentText()
        par = self.par_txtbox.toPlainText()

        match command:
            case "PUT":
                if not par:
                    self.output_txt.setPlainText('You must pass the file_name parameter to this function!')
                    return
                put(self, par)
            case "GET":
                if not par:
                    self.output_txt.setPlainText('You must pass the file_name parameter to this function!')
                    return            
                get(self, par)
            case "LS":
                if par:
                    self.output_txt.setPlainText('This function does not accept any paramters!')
                    return              
                list_files(self)
    
    def quit_pressed(self):
        client_socket.sendall("QUIT".encode(FORMAT))
        client_socket.close()
        exit()
    
    def show_popup(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Help")
        msg.setIcon(QtWidgets.QMessageBox.Information)

        msg.setText("""Call one of the following functions:\n\nPUT file_name:\nUpload a file to server\n\nLS:\nList of server files\n\nGET file_name:\nDownload a file from server""")

        msg.exec_()


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
is_connected = connect_to_server()
if not is_connected : exit()

client_dir_path = os.path.join(os.getcwd(), f'{client_socket.getsockname()[0]}, {client_socket.getsockname()[1]}')
os.mkdir(client_dir_path)


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
