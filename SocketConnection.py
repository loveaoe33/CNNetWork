import asyncio
import socket as sock

shared_variable = "FALSE"
ResponseText = ""


async def async_Socket(SocketMessage):
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
    global shared_variable
    shared_variable = "TRUE"
    global ResponseText
    ResponseText = response
    s.close()


async def async_Operation(SocketMessage):
    await async_Socket(SocketMessage)
    await asyncio.sleep(0.5)
    global shared_variable
    shared_variable = "FALSE"
    return "done," + ResponseText


async def main(SocketMessage):
    await async_Operation(SocketMessage)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(main("asdd"))
    else:
        asyncio.run(main("asds"), debug=True)
