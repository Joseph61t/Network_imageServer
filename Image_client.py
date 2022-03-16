# Server imports
import socket
# import sys
import os
from pathlib import Path
from PIL import Image

# Window imports
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfile

class IP_Manager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry = ('400x200')
        self.change_ip_button = ttk.Button(self, text='Set IP', command=lambda:self.change_ip())
        self.current_IP = "localhost"
        self.server_IP = tk.StringVar()
        self.IP_entry = tk.Entry(self, textvariable=self.server_IP)
        self.IP_entry.grid(row=0, column=0, pady=10)
        self.change_ip_button.grid(row=1, column=0, pady=10)
        self.wm_title("IP Manager")
    def change_ip(self):
        self.current_IP = self.server_IP.get()


class Network(tk.Tk):
    def __init__(self, host, port):
        super().__init__()
        self.HOST = host
        self.PORT = port
        # Create socket, and initialize parameters
        self.buffer_size = 4069
        self.sock = socket.socket()

        # Connect to server
        self.connect_server()

        # Create window elements
        self.title = "Image Network"
        self.title_thread = ""
        self.geometry = ('400x200')
        self.filepath = ""
        
        # Make label for choosing image
        # self.pick_image = ttk.Label(self, text='upload an image you want to save.')
        # self.pick_image.pack()
        # self.pick_image.grid(row=0, column=0, pady=10)
        
        # make button for choosing image
        self.choose_image_button = ttk.Button(self, text='Choose File', command=lambda:self.open_file())
        self.choose_image_button.grid(row=0, column=0, pady=10)
        # make name variable, label, and entry box
        self.get_name_label = tk.Label(self, text="Image Name")
        self.get_name_label.grid(row=2, column=0, pady=10)
        self.image_name = tk.StringVar()
        self.name_entry = tk.Entry(self, textvariable=self.image_name)
        self.name_entry.grid(row=3, column=0, pady=10)
        # make send button
        self.send_file_button = ttk.Button(self, text='Send Image', command=lambda:self.send_file())
        self.send_file_button.grid(row=0, column=1, pady=10)
        # make button for listing out all the files in the server's database
        self.list_files_button = ttk.Button(self, text="Available Files", command=lambda:self.list_files())
        self.list_files_button.grid(row=0, column=2, pady=10)
        # list of files in database when returned from list_files()
        self.file_list = tk.StringVar()
        # display of all files in server database when returned from list_files()
        self.file_list_label = tk.Label(self, textvariable=self.file_list)
        self.file_list_label.grid(row=2, column=3, pady=10)
        # make button for getting a file from server
        self.get_file_button = ttk.Button(self, text="Get File", command=lambda:self.get_file())
        self.get_file_button.grid(row=3, column=4, pady=10)

        self.wm_title(f"{self.title}")

    def connect_server(self):
        self.sock = socket.socket()
        # print(f"[+] Connecting to {self.HOST}:{self.PORT}")
        self.sock.connect((self.HOST, self.PORT))
        # print("[+] Connected.")
        # self.title_thread = self.sock.recv(self.buffer_size).decode()
        # self.title_thread = int(self.title_thread) + 1
        # self.wm_title(f"{self.title}: {self.title_thread}")
        # print(f"[+] Connected thread: {self.title_thread}")

    # open a file explorer, and allow the user to choose a file from their computer.
    def open_file(self):
        self.filepath = askopenfile(mode='r').name
        # self.filepath = self.filepath.replace("'","").replace("name=", "")
        # print(self.filepath)
        if self.filepath is not None:
            pass

    # sends a file to the server to be saved in the database
    def send_file(self):
        # print("getting name")
        name = self.image_name.get().replace(" ", "_")
        extension = str(self.filepath).split(".")[1]
        filesize = os.path.getsize(self.filepath)
        # print("Send file")
        self.sock.send(f"save,{name}.{extension},{filesize}".encode())
        # Make while loop to send packages of bytes to server.
        with open(self.filepath, "rb") as f:
            while True:
                bytes_read = f.read(self.buffer_size)
                if not bytes_read:
                    break
                self.sock.sendall(bytes_read)
        self.connect_server()
    
    # Returns all the files in the server, and displays them in file_list_display
    def list_files(self):
        data = "list, N/A, N/A"
        # Request the list of files in the database
        self.sock.sendall(data.encode())
        # Recieve file list from server
        files = self.sock.recv(self.buffer_size).decode()
        files = files.replace("[", "").replace("]", "").replace("'", "")
        # files = files.split(",")
        self.file_list.set(files)
        # print(files)
        self.connect_server()

    # gets a file from the server
    def get_file(self):
        name = self.image_name.get().replace(" ", "_")
        data = f"return,{name},N/A"
        self.sock.sendall(data.encode())

        recieved = self.sock.recv(self.buffer_size).decode()
        # print(recieved)
        name, size = recieved.split(",")
        size = int(size)
        name = str(Path.home()) + "\Downloads\\" + name
        with open(name, "wb") as f:
            # print("saving file")
            while True:
                # print("in-while")
                bytes_read = self.sock.recv(self.buffer_size)
                if not bytes_read:
                    break
                f.write(bytes_read)
        # self.sock.close()
        # print("opening file")
        image = Image.open(name)
        image.show()
        self.connect_server()


if __name__ == "__main__":
    ipManager = IP_Manager()
    ipManager.mainloop()
    HOST = ipManager.current_IP
    PORT = 9999
    Image_Network = Network(HOST, PORT)
    Image_Network.mainloop()
    # Image_Network.sock.close()