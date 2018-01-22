import socket

port = 60001
s = socket.socket()
host = ""

s.bind((host, port))
s.listen(5)

read_len = 1024 - 5

# filename = raw_input("Enter file to share:")
print 'Server listening....'

while True:
    conn, addr = s.accept()
    print 'Got connection from', addr

    while True:
        filename = conn.recv(1024)

        # Client closed the connection. handel code
        if filename == "end":
            break

        f = open(filename,'rb')
        l = f.read(read_len)
        while (l):
           conn.send("300"+l)
           print('Sent ',repr(l))
           l = f.read(read_len)
        conn.send("500")
        f.close()
    conn.close()
    print 'Connection closed'