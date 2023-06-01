import asyncio
import socket as sock
import GUIMain
import traceback
import tkinter as tk



shared_variable = "FALSE"
ResponseText = ""


def async_Socket(SocketMessage):
    global ResponseText
    try:
        host = "localhost"
        port = 8888
        s = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        s.connect((host, port))
        print('Python Client: Connected to Java server.')
        message = SocketMessage
        byte_data = message.encode()
        s.send(byte_data)
        response = s.recv(1024).decode()
        print("FromJavaMessage", response)
        ResponseText = response
        GUIMain.text_Response.insert(tk.END, "Socket連接成功\n")
        s.close()
    except Exception as e:
        ResponseText=""
        GUIMain.text_Response.insert(tk.END, traceback.format_exc() + "\n")


def async_Operation(SocketMessage):
    global ResponseText
    async_Socket(SocketMessage)
    if ResponseText=="":
        return ""
    else:
        return "done," + ResponseText


def main(SocketMessage):
     return  async_Operation(SocketMessage)
      

