"""
author: Roni Prital

date: november 2025

this is the client side of a
client server connection. the program
recieves a command from the client and
sends it to the server.
"""
import socket
import logging

IP = "127.0.0.1"
PORT = 6767
MAX_PACKET = 1024
INPUT_ERROR_MESSAGE = 'wrong command, try again'
SOCKET_ERROR = 'received socket error '
SCREENSHOT_PATH_LOCAL = r'.\screen.jpg'
USER_ORDERS = ('Hello, please enter\n'
               'DIR and file address for file content,\n'
               'DELETE and file address to delete file from folder,\n'
               'COPY and file address to copy file to folder,\n'
               'EXECUTE and file name to execute command,\n'
               'TAKE SCREENSHOT to take a screenshot,\n'
               'SEND_PHOTO to send the screenshot to user,\n'
               'EXIT to end the program run.\n'
               'enter command here:')


def user_input_check(user_input):
    """
    the function checks if the user input is a valid command, if it
    is the function returns true if it is not the function
    returns false.
    """
    if user_input == "TAKE_SCREENSHOT" or user_input == "SEND_PHOTO" \
       or user_input[:3] == "DIR" or user_input[:6] == "DELETE" \
       or user_input[:4] == "COPY" or user_input[:7] == "EXECUTE" \
       or user_input == "EXIT":
        return True
    else:
        return False


def client():
    """
    the function runs the client.
    handles some of the commands that
    are needed in the client side.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((IP , PORT))
        logging.info("connected to server on 127.0.0.1 , 6767")

        while True:
            user_input = input(USER_ORDERS)

            if  not user_input_check(user_input):
                print(INPUT_ERROR_MESSAGE)
                continue

            client_socket.send(user_input.encode())

            if user_input == "TAKE_SCREENSHOT":
                    response = client_socket.recv(MAX_PACKET).decode()
                    print(response)
                    continue

            if user_input == "SEND_PHOTO":
                with open(SCREENSHOT_PATH_LOCAL, "wb") as f:
                    while True:
                        data = client_socket.recv(MAX_PACKET)
                        if not data:
                            break
                        f.write(data)
                print("screenshot received successfully")

                client_socket.close()
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((IP, PORT))
                continue

            if user_input == "EXIT":
                    response = client_socket.recv(MAX_PACKET).decode()
                    print(response)
                    break

            response = client_socket.recv(MAX_PACKET).decode()
            print(response)

    except socket.error as err:
        print(SOCKET_ERROR + str(err))
    finally:
        client_socket.close()


def main():
    client()


if __name__ == '__main__':
    log_format = '%(levelname)s: %(message)s'
    log_level = logging.DEBUG
    logging.basicConfig(level=log_level, format=log_format)
    main()