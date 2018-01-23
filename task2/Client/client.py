import socket                   
import json
import time

s = socket.socket()             
host = ""
port = 60001

s.connect(('10.42.0.106', port))

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

total_time = 0

while True:
	# Prompt the user to enter filename or --list
	filename = raw_input('Enter a filename or --list to see the list of files available ')

	start_time = time.clock()
	if filename == 'disconnect':
		request = get_request('disconnect', '')
		s.send(json.dumps(request))
		break
	elif filename == '--list':
		request = get_request('list','')
		s.send(json.dumps(request))
		response = json.loads(s.recv(1024 + 45))
		display_files(response)
	else:
		request = get_request('file-data',filename)
		s.send(json.dumps(request))
		response = receive_file(s, filename)
		display_status(response)

	total_time += (time.clock()-start_time)
	print "Total time taken is ",total_time

s.close()
print('connection closed')