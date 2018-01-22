#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>
#include <netinet/in.h>
#define PORT 8080
int main(int argc, char const *argv[]) {
    int server_fd, new_socket, valread;
    // sockaddr_in - references elements of the socket address. "in" for internet
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    char buffer[1024] = {0};

    // Creating socket file descriptor
    // creates socket, SOCK_STREAM is for TCP. SOCK_DGRAM for UDP
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    // This is to lose the pesky "Address already in use" error message
    // SOL_SOCKET is the socket layer itself
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEPORT,&opt, sizeof(opt))) {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }
    address.sin_family = AF_INET;  // Address family. For IPv6, it's AF_INET6. 29 others exist like AF_UNIX etc. 
    address.sin_addr.s_addr = INADDR_ANY;  // Accept connections from any IP address - listens from all interfaces.
    address.sin_port = htons( PORT );    // Server port to open. Htons converts to Big Endian - Left to Right. RTL is Little Endian

    // Forcefully attaching socket to the port 8080
    if (bind(server_fd, (struct sockaddr *)&address,sizeof(address))<0) {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }

    // Port bind is done. You want to wait for incoming connections and handle them in some way.
    // The process is two step: first you listen(), then you accept()
    // 3 is the maximum size of queue - connections you haven't accepted
    if (listen(server_fd, 3) < 0) {
        perror("listen");
        exit(EXIT_FAILURE);
    }

    while(1) {
        // returns a brand new socket file descriptor to use for this single accepted connection. Once done, use send and recv
        struct sockaddr_in cliaddr;
        if ((new_socket = accept(server_fd, (struct sockaddr *)&cliaddr,(socklen_t*)&addrlen))<0) {
            perror("Error in Accepting New Connection");
            close(new_socket);
            continue;
        }

        // Reading file name requested by client.
        // read infromation received into the buffer
        valread = read(new_socket , buffer, 1024);
        if(valread == -1) {
            perror("failed to read filename from client");
            close(new_socket);
            continue;
        }
        buffer[valread] = '\0';

        // Opening the file requested by the client.
        int fd;
        if ( (fd= open(buffer,O_RDONLY)) < 0) {
            perror("failed to open the requested file");
            close(fd);
            close(new_socket);
            continue;
        }

        int read_status = 1;

        valread = read(fd,buffer,1024);
        if (valread == -1) {
            perror("Failed to read the requested file");
            close(fd);
            close(new_socket);
            continue;
        }

        // Read 1024 bytes at once and sending to the client.
        while(valread) {
            send(new_socket,buffer,valread,0);
            valread = read(fd,buffer,1024);
            if (valread == -1) {
                perror("Failed to read the requested file");
                close(fd);
                close(new_socket);
                read_status = -1;
                break;
            }            
        }

        if(read_status != -1) {
            printf("File successfully sent to the client\n");
            close(new_socket);
        }
    }

    return 0;
}
