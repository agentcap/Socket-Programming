import socket                   

s = socket.socket()             
host = ""
port = 60001                

s.connect(('10.42.0.106', port))
# s.send("Hello server!")
while True:
	filename = raw_input('Enter a filename ')
	s.send(filename)
	if filename == 'end':
		break
	with open(filename, 'wb') as f:
	    print 'file opened'
	    while True:
	        print('receiving data...')
	        data = s.recv(1024)
	        code = data[0:3]
	        if code == '500':
	        	break
	        data = data[3:]
	        print('data=%s', (data))
	        # write data to a file
	        f.write(data)

	f.close()
	print('Successfully get the file')
s.close()
print('connection closed')
