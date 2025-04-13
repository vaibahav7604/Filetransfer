import os,socket,ssl


Server_host='0.0.0.0'
port=5001
buffer_size=8192
Separator='<SEPARATOR>'

os.makedirs('received_files',exist_ok=True)

server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((Server_host,port))
server_socket.listen(5)
print(f"Server is listening on {Server_host}:{port}")

def ProgreddBar(current,total,bar_length=50):
    percent = current / total
    filled_length = int(bar_length * percent)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f'\r|{bar}| {percent:.2%} ({current}/{total} bytes)', end='')

while True:
    try:
        client_socket,addr=server_socket.accept()
        
        # receive the file info
        received=client_socket.recv(buffer_size).decode()
        filename,size=received.split(Separator)
        filename=os.path.basename(filename)
        size=int(size)
        MB=round(size/1000000,2)
        print(f"Receiving : {filename} of size {MB} MB")


        # saves teh incoming files

        filepath=os.path.join("received_files",filename)
        with open(filepath,'wb') as f:
            bytes_received=0
            while bytes_received<size:
                bytes_read=client_socket.recv(buffer_size)
                if not bytes_read:
                    break
                f.write(bytes_read)
                bytes_received+=len(bytes_read)
                ProgreddBar(bytes_received,size)
        print(f"\n[+] File {filename} received successfully")
        client_socket.close()

    except KeyboardInterrupt:
        print("\n[+] Server stopped by user")
        break
    except Exception as e:
        print(f"[!] Error: {e}")
        break
    finally:
        server_socket.close()
        print("[+] Server closed")
