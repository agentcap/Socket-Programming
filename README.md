# Change IP Addresses.

# Assignment - 1

## Team members:

- NAME1: MNS Subramanyam 
- Rollnumber No1 : 20161190

- NAME2: Sree Ram Sai Pradeep Yarlagadda
- Rollnumber No2 : 20161164


## Directory structure
.
├── Q1
│   ├── client
│   │   └── client.c
│   └── server
│       └── server.c
├── Q2
│   ├── client
│   │   ├── client_nonpersistent.c
│   │   └── client_persistent.c
│   └── server
│      	├── c
│       ├── server_nonpersistent.c
│       └── server_persistent.c
└── README.md

## How to run the code 

### Q1

#### Usage

- Go to Server directory.

	gcc server.c -o server
	./server

- Go to Client directory.

	gcc client.c -o client
	./client <file name to be downloaded from server>

### Q2

#### Persistent

- Go to Server directory.

	python server_persistent.py

- Go to Client directory.
	
	python server_persistent.py

#### Non-Persistent

- Go to Server directory.

	python server_nonpersistent.py

- Go to Client directory.
	
	python client_nonpersistent.py

### Observations for Persistent and Non-Persistent Connections

#### Cumulative timings for Persistent connection
- 0.001446s --> time taken for file1 to be copied 
- 0.002599s --> time taken for file1, file2 to be copied
- 0.014781s --> time taken for file1, file2, file3 to be copied

#### Cumulative timings for Persistent connection

- 0.001611s --> time taken for file1 to be copied 
- 0.003002s --> time taken for file1, file2 to be copied
- 0.019561s --> time taken for file1, file2, file3 to be copied

- In non-persistent connection new socket is created and used each time for file transfer.
- Whereas in persistent connection same socket is used for all the files.
- Hence persistent connection takes less time than non-persistent connection.