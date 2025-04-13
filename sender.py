'''✅ Complete Data Flow:
User selects a file

Client connects to server

Sends metadata (filename, filesize)

Opens file in binary mode

Reads file in chunks

Sends each chunk

Closes connection'''

import socket,os
from tkinter import filedialog,Tk

Server_host='192.168.31.120'#add your ip using config tcpv4
port=5001
buffer_size=8192
Separator='<SEPARATOR>'
try:
    # Initialize Tkinter root window (hidden)
    root = Tk()
    root.withdraw()  # Hide the root window

    # Open file picker dialog
    filename = filedialog.askopenfilename(title="Select a file to send")

    if not filename:
        print("No file selected. Exiting.")
        exit()

    size = os.path.getsize(filename)

    client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client_socket.connect((Server_host,port))
    except ConnectionRefusedError:
        print("could Not connect ")
        exit()
    client_socket.send(f"{filename}{Separator}{size}".encode())

    with open(filename,'rb') as f:
        while True:
            bytes_read=f.read(buffer_size)
            if not bytes_read:
                break
            client_socket.sendall(bytes_read)
        print(f"sended Successfully{filename}")
except Exception as e:
    print(f"Not expected :{e}")
finally:
    # Close the client socket
    client_socket.close()
