# Overview

This is a simple server and client combination, the server controls an image database, and can send the client a requested image, or a list of all the images in the database. It can also recieve an image, and save it to the database.


To start the server, you simply need to run the python program named Image_server.py in the NETWORK_IMAGESERVER file.

the client side is even simpler, you just need to run the Image_client.exe program, and it will start up.

A window for entering the server IP address will open, (which you can get from the start up sequence of the server.) and on setting the IP, it will open the client window.

You can then use the contents of that window to send and recieve things from the server. Every image that is sent to the server needs to have a name atached to it, which the server will use to store the image. That same name, along with the added extension (extracted from the filepath choosen). These can all be viewed by clicking the available files button which will extend the window, displaying all images in the Database. Names will have all spaces removed, and replaced with "_" for better file management.

The orignal idea was to provide a quick way to share images with other people.



[Software Demo Video](https://youtu.be/ZQe9SwPhXcE)

# Network Communication

I used Client/Server to make this.

I used TCP for this program, and threading to make it possible to open multiple client windows on multiple computers, so long as they are all on the same network. So long as the network allows comunication between computers that are on it. (ie. not the school network.)

I used a string seperated by commas (ex. "command,name,filesize") If a command that doesn't need any of the two other parameters is sent, those variables will be replaced with N/A.

# Development Environment

I used visual studio code, and am saving it all to github.

I used python for these programs. I used the socket, os, pathlib, PIL, threading, and the tkinter libraires for the programs.

# Useful Websites


* [python.org](http://docs.python.org)


# Future Work

* Error handling, if someone tries to send an image without giving it a name, or get an image without specifying a name, or adding the correct extension.
* User managment, only allow certain programs to access the server, possibly by asking for a key before connecting, and if the incorrect key is given, not allowing the connection through. The key could be saved to a seperate file, and read if it exists. 
* Make the IP easier to enter or not need to be entered.