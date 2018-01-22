all :
	gcc server.c -o server
	gcc client.c -o client

clean :
	rm -r server client