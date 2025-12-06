"""
author: Roni Prital

date: november 2025

the server side of a client
server connection.
the program handles the clients
requests and sends them back to the client.
"""
import socket
import logging
import os
import glob
import shutil
import subprocess
import pyautogui

IP = "127.0.0.1"
PORT = 6767
QUEUE_LEN = 1
MAX_PACKET = 1024
SOCKET_ERROR = 'communication error'
SCREENSHOT_PATH = r'.\screen.jpg'
FILE_DOESNOT_EXIST = 'file does not exist'
FILE_DELETE = 'file removed'
FILE_WAS_NOT_DELETED = 'file can not be removed'
FILE_COPIED = 'file copied'
FILE_WAS_NOT_COPIED = 'file did not copy'
PROG_EXES = 'program executed'
NO_PROG = 'program not executed'


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


def folder_content(folder_name):
    """
    the function returns all the files
    in a folder (DIR command) if the folder
    does not  exist it returns an error.
    """
    if not os.path.exists(folder_name) or not os.path.isdir(folder_name):
        return FILE_DOESNOT_EXIST
    try:
        files_list = glob.glob(folder_name + r'\*.*')
        return str(files_list)
    except:
        return FILE_DOESNOT_EXIST


def delete_file(file_to_remove_name):
    """
    the function deletes a file
    if the file doesn't exist,
    it returns an error.
    """
    if not os.path.exists(file_to_remove_name):
        return FILE_WAS_NOT_DELETED
    try:
        os.remove(file_to_remove_name)
        return FILE_DELETE
    except:
        return FILE_WAS_NOT_DELETED


def copy_file(file_copy_name, where_to_copy):
    """
    the function copies a file and if the file
    doesn't exist, it returns an error.
    """
    if not os.path.exists(file_copy_name):
        return FILE_WAS_NOT_COPIED
    try:
        shutil.copy(file_copy_name, where_to_copy)
        return FILE_COPIED
    except:
        return FILE_WAS_NOT_COPIED


def exe_prog(program_to_run):
    """
    the function executes a program,
    if the program doesn't exist it
    returns an error.
    """
    try:
        subprocess.call(program_to_run)
        return PROG_EXES
    except:
        return NO_PROG


def take_screenshot ():
    """
    the function takes a screenshot and saves it to a file, returns as bytes.
    """
    image = pyautogui.screenshot()
    image.save(SCREENSHOT_PATH)
    with open(SCREENSHOT_PATH, 'rb') as f:
        return f.read()


def server():
    """
    the function runs the server and
    calls all the needed functions for
    the right input.
    """
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((IP , PORT))
        server_socket.listen(QUEUE_LEN)
        logging.info("server on, listening on port 6767")
        client_socket, client_address = server_socket.accept()
        try:
            while True:
                user_input = client_socket.recv(MAX_PACKET).decode()
                if user_input_check(user_input):

                    if user_input[:3] == "DIR":
                        logging.info("the user's info is: DIR \n returning all files in given folder.")
                        response = folder_content(user_input[4:])
                        client_socket.send(response.encode())
                        continue

                    if user_input[:6] == "DELETE":
                        logging.info("the user's input is: DELETE \n removing given file.")
                        response = delete_file(user_input[7:])
                        client_socket.send(response.encode())
                        continue

                    if user_input[:4] == "COPY":
                        logging.info("the user's input is: COPY \n copying file.")
                        response = copy_file(user_input[5:])
                        client_socket.send(response.encode())
                        continue

                    if user_input[:7] == "EXECUTE":
                        logging.info("the user's input is: EXECUTE \n executing given program.")
                        response = exe_prog(user_input[8:])
                        client_socket.send((response).encode())
                        continue

                    if user_input == "TAKE_SCREENSHOT":
                        logging.info("the user's input is: TAKE_SCREENSHOT \n "
                                     "taking a screenshot and saving it to a file.")
                        take_screenshot()
                        client_socket.send("screenshot taken".encode())
                        continue

                    if user_input == "SEND_PHOTO":
                        logging.info("the user's input is: SEND_PHOTO \n sending photo. ")
                        with open(SCREENSHOT_PATH, 'rb') as f:
                            image_bytes = f.read()
                        client_socket.send(image_bytes)
                        client_socket.close()
                        client_socket, client_address = server_socket.accept()
                        continue

                    if user_input == "EXIT":
                        client_socket.send(("goodbye").encode())
                        client_socket.close()
                        client_socket, client_address = server_socket.accept()
                        continue
                else:
                    client_socket.send("Error, command does not exist".encode())
        except socket.error as error:
            print (SOCKET_ERROR + str(error))
        finally:
            client_socket.close()
    except socket.error as error2:
        print (SOCKET_ERROR + str(error2))
    finally:
        server_socket.close()


def main():
    server()


if __name__ == '__main__':
    log_format = '%(levelname)s: %(message)s'
    log_level = logging.DEBUG
    logging.basicConfig(level=log_level, format=log_format)
    assert delete_file("non_existing_file.txt") == FILE_WAS_NOT_DELETED
    assert copy_file("non_existing_file.txt", "./") == FILE_WAS_NOT_COPIED
    assert folder_content("non_existing_folder") == FILE_DOESNOT_EXIST
    main()