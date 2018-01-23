import socket                   
import json

def get_request(type, data):
	request = {}
	request['type'] = type
	request['data'] = data
	return request

def receive_file(s, filename):
	temp = s.recv(1024)
	response = json.loads(temp)
	status = response['status']
	if status == '404':
		return response

	with open(filename, 'wb') as file:
	    while True:
	        status = response['status']
	        if status == '500':
	        	file.close()
	        	return response

	        data = response['data']
	        file.write(data)
	        temp = s.recv(1024)
	        response = json.loads(temp)

	file.close()

def display_files(response):
	if response['status'] == '403':
		print response['data']
	else:
		print('Files list')
		for file in response['data']:
			print(file)

def display_status(response):
	print(response['data'])

host = ""
port = 60001


while True:
	# Prompt the user to enter filename or --list
	filename = raw_input('Enter a filename or --list to see the list of files available ')
	s = socket.socket()             
	s.connect(('10.42.0.106', port))

	if filename == '--list':
		request = get_request('list','')
		s.send(json.dumps(request))
		response = json.loads(s.recv(1024 + 45))
		display_files(response)
	else:
		request = get_request('file-data',filename)
		s.send(json.dumps(request))
		response = receive_file(s, filename)
		display_status(response)

	s.close()
	print('connection closed')
	