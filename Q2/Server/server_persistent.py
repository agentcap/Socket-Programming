import socket
from os import listdir
import json
import time

def list_files (directory):
    """
        This function takes the name of the directory 
        and returns json object along with status ,type of 
        response and the data having list of file 
    """
    response = {}
    try:
        list = listdir(directory);
        response["type"] = "data"
        response["status"] = "300"
        response["data"] = list

    except Exception as e:
        response["type"] = "mssg"
        response["status"] = "403"
        response["data"] = "Unable to get the list of files"

    return response

def is_file(filename):
    """
        This function takes the filename and return whether
        the given filename is present in the share_dir
    """
    return filename in listdir(share_dir)


def error_handler(status,error):
    """
        This function takes the status code and error message
        and return json object having response.
    """
    response = {}
    response["type"] = "mssg"
    response["status"] = status
    response["data"] = error

    return response

def send_file(conn,filename):
    """
        This function takes the socket and the filename
        and send the contents of the file along with 
        response code and handle the error responses.
    """
    try:
        file = open(share_dir+'/'+filename,'rb')
        # 45 bytes for the json object along with status and type
        # And the rest is for the contents of the file.
        data = file.read(1024-45)
        response = {}
        response["type"] = "file"
        response["status"] = "300"
        while (data):
            response["data"] = data
            conn.send(json.dumps(response))
            time.sleep(0.1)
            data = file.read(1024 - 45)

        # If Succsessfully sent the whole file the fucntion return
        # response with status "500"
        response["type"] = "tran"
        response["status"] = "500"
        response["data"] = "File " + filename + " transfered successfully"

        file.close()
    except Exception as e:
        response = error_handler("404","Failed to read the file")

    return response

def server (host,port):
    """
        This function takes the host and port address as input
        and runs the server accepting connections
    """
    try:
        sock = socket.socket()
        sock.bind((host, port))
        sock.listen(5)
    except Exception as e:
        print("Failed to create and bind the socket")

    print 'Server listening on port ',port

    while True:
        # Accepting the request from client
        conn, addr = sock.accept()
        print 'Got connection from', addr

        while True:
            response = {}

            # Receving the request from client and converting to json
            try:
                request = json.loads(conn.recv(1024))
            except Exception as e:
                response = error_handler("404","Invalid Request Format")

            # Handling the disconnect request from client
            try:
                if request["type"] == "disconnect":
                    break
            except Exception as e:
                response = error_handler("403","Failed to Disconnect")

            # Handling the list request from client
            try:
                if request["type"] == "list":
                    response = list_files(share_dir)
            except Exception as e:
                response = error_handler("403","Request field 'type' is missing")

            # Handling the file request from client
            try:
                if request["type"] == "file-data":
                    if is_file(request["data"]):
                        response = send_file(conn,request["data"])
                    else :
                        response = error_handler("404","Not a valid File name")
            except Exception as e:
                response = error_handler("404","Request field 'type' is missing")

            # Printing the response after sending th file/any error occured
            try:
                print(response)
                conn.send(json.dumps(response))
            except Exception as e:
                time.sleep(2)
                print"Connection Broken with ", addr


        conn.close()
        print 'Connection closed' ,addr


port = 60001
host = ""
share_dir = 'Data'

server(host,port)