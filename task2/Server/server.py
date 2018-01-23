import socket
from os import listdir
import json
import time

def list_files (directory):
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
    return filename in listdir(share_dir)


def error_handler(status,error):
    response = {}
    response["type"] = "mssg"
    response["status"] = status
    response["data"] = error

    return response

def send_file(conn,filename):
    try:
        file = open(share_dir+'/'+filename,'rb')
        data = file.read(1024-45)
        response = {}
        response["type"] = "file"
        response["status"] = "300"
        while (data):
            response["data"] = data
            conn.send(json.dumps(response))
            time.sleep(0.1)
            data = file.read(1024 - 45)

        response["type"] = "tran"
        response["status"] = "500"
        response["data"] = "File " + filename + " transfered successfully"

        file.close()
    except Exception as e:
        response = error_handler("404","Failed to read the file")

    return response

def server (host,port):

    try:
        sock = socket.socket()
        sock.bind((host, port))
        sock.listen(5)
    except Exception as e:
        print("Failed to create and bind the socket")

    print 'Server listening on port ',port

    while True:
        conn, addr = sock.accept()
        print 'Got connection from', addr

        while True:
            response = {}
            try:
                request = json.loads(conn.recv(1024))
            except Exception as e:
                response = error_handler("404","Invalid Request Format")

            try:
                if request["type"] == "disconnect":
                    break
            except Exception as e:
                response = error_handler("403","Failed to Disconnect")

            try:
                if request["type"] == "list":
                    response = list_files(share_dir)
            except Exception as e:
                response = error_handler("403","Request field 'type' is missing")

            try:
                if request["type"] == "file-data":
                    if is_file(request["data"]):
                        response = send_file(conn,request["data"])
                    else :
                        response = error_handler("404","Not a valid File name")
            except Exception as e:
                response = error_handler("404","Request field 'type' is missing")

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