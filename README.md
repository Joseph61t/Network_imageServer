# Overview

This is a simple server and client combination, the server controls an image database, and can send the client a requested image, or a list of all the images in the database. It can also recieve an image, and save it to the database.

To start the server, you simply need to run the python program named Image_server.py in the NETWORK_IMAGESERVER file. the client side is much the same, run the Image_client.py in that same folder. A window will open, and you can then use the contents of that window to send and recieve things from the server. Every image that is sent to the server needs to have a name atached to it, which the server will use to store the image. That same name, along with the added extension (extracted from the filepath choosen). These can all be viewed by clicking the available files button which will extend the window, displaying all images in the Database. Names will have all spaces removed, and replaced with "_" for better file management.

The orignal idea was to provide a quick way to share images with other people.



[Software Demo Video](https://youtu.be/d-_QmHsGw6I)

# Network Communication

I used Client/Server to make this.

I used TCP for this program, and used port 9999

I used a string seperated by commas (ex. "command,name,filesize") If a command that doesn't need any of the two other parameters is sent, those variables will be replaced with N/A.

# Development Environment

I used visual studio code, and am saving it all to github.

I used python for these programs. I used the socket, os, pathlib, PIL, and the tkinter libraires for the programs.

# Useful Websites


* [python.org](http://docs.python.org)


# Future Work

* Error handling, if someone tries to send an image without giving it a name, or get an image without specifying a name, or adding the correct extension
* Make this usable with multiple computers.
* Add multi-threading