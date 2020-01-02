#define _WIN32_WINNT 0x501
#include <winsock2.h>
#include <ws2tcpip.h>
#include <stdio.h>
#pragma comment(lib, "Ws2_32.lib")

#define DEFAULT_PORT "1802"

int main() {
	WSADATA wsaData;
	int iResult,iSendResult;
	struct addrinfo *result = NULL, *ptr = NULL, hints;
	char recvbuf[512];
	int recvbuflen = 512;

	iResult = WSAStartup(MAKEWORD(2, 2), &wsaData);
	if (iResult != 0) {
		printf("WSAStartup failed: %d\n", iResult);
		return 1;
	}
	printf("NO error");

	ZeroMemory(&hints, sizeof(hints));
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_STREAM;
	hints.ai_protocol = IPPROTO_TCP;
	hints.ai_flags = AI_PASSIVE;
	iResult = getaddrinfo(NULL, DEFAULT_PORT, &hints, &result);
	if (iResult != 0) {
		printf("getaddrinfo failed: %d\n", iResult);
		WSACleanup();
		return 1;
	}
	printf("\nGet addr_info succesful");

	SOCKET serversock = INVALID_SOCKET;
	SOCKET clientsock;
	serversock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
	if (serversock == INVALID_SOCKET) {
		printf("Error at socket(): %ld\n", WSAGetLastError());
		freeaddrinfo(result);
		WSACleanup();
		return 1;
	}
	printf("\nSocket creation succesfull");
	//binding
	iResult = bind(serversock, result->ai_addr, (int)result->ai_addrlen);
	//printf("1");
	if (iResult == SOCKET_ERROR) {
		printf("bind failed with error: %d\n", WSAGetLastError());
		freeaddrinfo(result);
		closesocket(serversock);
		WSACleanup();
		return 1;
	}
	printf("\nbind succesfull");

	do {
		//listening
		if (listen(serversock, SOMAXCONN) == SOCKET_ERROR) {
			printf("Listen failed with error: %ld\n", WSAGetLastError());
			closesocket(serversock);
			WSACleanup();
			return 1;
		}
		printf("\nlistening");

		//accepting connection
		
		clientsock = accept(serversock, NULL, NULL);
		printf("e");
		if (clientsock == INVALID_SOCKET) {
			printf("accept failed: %d\n", WSAGetLastError());
			closesocket(serversock);
			WSACleanup();
			return 1;
		}
		printf("Connection established");
		do {
			iResult = recv(clientsock, recvbuf, recvbuflen, 0);
			printf("\n %s \n", recvbuf);
			if (iResult > 0) {
				printf("Bytes received: %d\n", iResult);
				system("start vlc :sout=#transcode{vcodec=h264,scale=Auto,acodec=mpga,ab=128,channels=2,samplerate=44100,scodec=none}:duplicate{dst=rtp{sdp=rtsp://:8554/s1},dst=display} :sout-all :sout-keep);
				// Echo the buffer back to the sender
				printf("Stream Started\n");
				/*
				iSendResult = send(clientsock,"Hi Voreshwar", iResult, 0);
				if (iSendResult == SOCKET_ERROR) {
					printf("send failed: %d\n", WSAGetLastError());
					closesocket(clientsock);
					WSACleanup();
					return 1;
				}
				printf("Bytes sent: %d\n", iSendResult);*/
			}
			if (iResult == 18) {
				printf("Task Kill");
				system("taskkill /IM vlc.exe /f");
			}
			/*if (iResult == 0) {
				printf("Connection closing...\n");
			}
			else {
				printf("recv failed: %d\n", WSAGetLastError());
				//system("taskkill /IM vlc.exe /f");
				//closesocket(clientsock);
				//WSACleanup();
				return 1;
			} */
		} while (iResult != 18);

	} while (1);
	return 0;
}