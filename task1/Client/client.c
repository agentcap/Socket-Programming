// Client side C/C++ program to demonstrate Socket programming
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>
#define PORT 8080

int main(int argc, char const *argv[])
{
    struct sockaddr_in address;
    int sock = 0, valread;
    struct sockaddr_in serv_addr;
    char *filename;
    char buffer[1024] = {0};

    //Getting file name from client.
    if(argc != 2) {
        printf("Usage ./client [filename]\n");
        return 0;
    }
    filename = (char *)argv[1];

    if((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("Socket creation error");
        return -1;
    }

    // to make sure the struct is empty. Essentially sets sin_zero as 0
    // which is meant to be, and rest is defined below
    memset(&serv_addr, '0', sizeof(serv_addr));

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);

    // Converts an IP address in numbers-and-dots notation into either a 
    // struct in_addr or a struct in6_addr depending on whether you specify AF_INET or AF_INET6.
    if(inet_pton(AF_INET, "10.42.0.106", &serv_addr.sin_addr)<=0) {
        perror("Invalid address/ Address not supported");
        return -1;
    }

    // connect to the server address
    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        perror("Connection Failed");
        close(sock);
        return -1;
    }
    printf("Connection Established successfully\n");

    // send the required filename to the client.
    if(send(sock , filename , strlen(filename) , 0 ) == -1) {
        close(sock);
        perror("Failed to send filename to the server");
        return -1;
    }
    printf("File name sent successfully\n");

    // open/create a new file to write the data received from the buffer.
    int fd = open(filename, O_CREAT | O_WRONLY | O_TRUNC, 0600);
    if(fd < 0) {
        close(sock);
        close(fd);
        perror("Unable to open/create the file");
        exit(EXIT_FAILURE);
    }

    // receive message back from server, into the buffer
    valread = read( sock , buffer, 1024);  
    if(valread < 0) {
        close(sock);
        close(fd);
        perror("Unable to read message sent from server");
        exit(EXIT_FAILURE);
    }

    //Read 1024 bytes at once from the server and write to the file created/opened.
    while(valread) {
        if(write(fd, buffer, valread) < 0) {
            close(sock);
            close(fd);
            perror("Unable to write to the file");
            exit(EXIT_FAILURE);
        }
        valread = read(sock, buffer, 1024); 
        if(valread < 0) {

            perror("Unable to read message sent from server");
            exit(EXIT_FAILURE);
        }
    }
    printf("Requested file has been successfully downloaded from server\n");
    return 0;
}