import socket
import os
import logging
import threading
class client_thread:
    def __init__(self, socket, address, thread):
        self.thread_name = "thread " + str(thread)
        self.client_socket = socket
        self.address = address
        self.buffer_size =  4096

    def handle_thread(self):
        while True: 
            data = self.client_socket.recv(self.buffer_size).decode()
            if len(data) == 0:
                self.client_socket.close()
                print("Closed Connection")
                break
            doing, name, size = data.split(",")
            name = "Database/" + name
            print(doing)
            if doing == "save":
                self.save_image(name, size)
                break
            elif doing == "list":
                self.return_list()
                break
            elif doing == "return":
                self.return_image(name)
                break

    # Save the file to the database file
    def save_image(self, name, size):
        size = int(size)
        with open(name, "wb") as f:
            while True:
                print("[+]")
                bytes_read = self.client_socket.recv(self.buffer_size)
                if not bytes_read:
                    break
                f.write(bytes_read)
            self.client_socket.close()
            print("[O]")
    
    # Return the list of all files in database file
    def return_list(self):
        self.client_socket.send(str(os.listdir("Database")).encode())
    
    # Return the image requested
    def return_image(self, name):
        filesize = os.path.getsize(name)
        name = name.replace("Database/", "")

        self.client_socket.send(f"{name},{filesize}".encode())
    
        with open(f"Database/{name}", "rb") as f:
            while True:
                bytes_read = f.read(self.buffer_size)
                if not bytes_read:
                    break
                self.client_socket.sendall(bytes_read)
            self.client_socket.close()


class server:
    def __init__(self, HOST, PORT):
        self.sock = socket.socket()
        self.sock.bind((HOST, PORT))
        self.buffer_size =  4096
    
    def create_thread(self, thread):
        new_thread = client_thread(self.client_socket, self.address, thread)
        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

        logging.info("Main   : before creating thread")
        x = threading.Thread(target=new_thread.handle_thread)
        logging.info("Main   : before running thread")
        x.start()
        logging.info("Main   : wait for the thread to finish")
        x.join()
        logging.info("Main   : all done")

    def handle_server(self):
        thread_count = 0
        self.sock.listen(5)
        print(f"[*] Listening as {HOST}:{PORT}")
        while True:
            self.client_socket, self.address = self.sock.accept()
            print(f"{self.address} connected.")
            thread_count += 1
            self.create_thread(thread_count)


def get_ip():
    return socket.gethostbyname(socket.gethostname())


if __name__ == "__main__":
    HOST = get_ip()
    print(HOST)
    PORT = 9999
    Image_Server = server(HOST, PORT)
    Image_Server.handle_server()
