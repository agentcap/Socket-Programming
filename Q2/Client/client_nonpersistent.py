import socket                   
import json
import time

def get_request(type, data):
	"""
		This function takes type of request ,data and
		return the json of the request.
	"""
	request = {}
	request['type'] = type
	request['data'] = data
	return request

def receive_file(s, filename):
	"""
		This function takes the socket and filename 
		and save the content recived from the socket into
		the filename given
	"""
	temp = s.recv(1024)
	response = json.loads(temp)
	status = response['status']

	# If the status 404 It means wrong filename
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
	""" This function takes response and print the file names"""
	if response['status'] == '403':
		print response['data']
	else:
		print('Files list')
		for file in response['data']:
			print(file)

def display_status(response):
	"""This function displays the status of the respons"""
	print(response['data'])

host = ""
port = 60001

total_time = 0

while True:
	# Prompt the user to enter filename or --list
	filename = raw_input('Enter a filename or --list to see the list of files available ')
	start_time = time.clock()
	s = socket.socket()             
	s.connect(('10.42.0.106', port))

	 # It the client request for list of files
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

	total_time += (time.clock()-start_time)
	s.close()
	print "Total time taken is ", total_time
	print('connection closed')
	