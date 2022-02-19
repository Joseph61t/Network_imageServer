import socket
import os

HOST, PORT = "localhost", 9999
buffer_size =  4096

sock = socket.socket()
sock.bind((HOST, PORT))

sock.listen(5)
print(f"[*] Listening as {HOST}:{PORT}")
while True:
    client_socket, address = sock.accept()
    print(f"{address} connected.")
    while True:
        data = client_socket.recv(buffer_size).decode()
        if len(data) == 0:
            client_socket.close()
            print("Closed Connection")
            break
        doing, name, size = data.split(",")
        name = "Database/" + name
        print(doing)
        if doing == "save":
            size = int(size)
            with open(name, "wb") as f:
                while True:
                    print("[+]")
                    bytes_read = client_socket.recv(buffer_size)
                    if not bytes_read:
                        break
                    f.write(bytes_read)
                client_socket.close()
                print("[O]")
                break

        elif doing == "list":
            client_socket.send(str(os.listdir("Database")).encode())

        elif doing == "return":
            filesize = os.path.getsize(name)
            name = name.replace("Database/", "")
                # name.append(".")
                # sock.send(f"{name},{filesize}".encode())
            client_socket.send(f"{name},{filesize}".encode())

            with open(f"Database/{name}", "rb") as f:
                while True:
                    bytes_read = f.read(buffer_size)
                    if not bytes_read:
                        break
                    client_socket.sendall(bytes_read)
                client_socket.close()
                break

        else:
            client_socket.close()