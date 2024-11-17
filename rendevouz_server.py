import socket

SERVER_IP = "0.0.0.0"  #all
SERVER_PORT = 5000    

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        server_socket.bind((SERVER_IP, SERVER_PORT))
        print(f"Server starts listen on {SERVER_IP}:{SERVER_PORT}.")
        
        clients = {} 

        while True:
            data, addr = server_socket.recvfrom(1024)
            print(f"Received a message from {addr}: {data.decode()}.")
            
            if addr not in clients:
                clients[addr] = data.decode()  
                print(f"New client: {addr}.")
            
            if len(clients) == 2:
                client_list = list(clients.keys())
                client1, client2 = client_list[0], client_list[1]

                server_socket.sendto(f"{client2[0]}:{client2[1]}".encode(), client1)
                server_socket.sendto(f"{client1[0]}:{client1[1]}".encode(), client2)

                print(f"Exchanged client info between {client1} and {client2}.")
                
                clients = {}

    except KeyboardInterrupt:
        print("shutting down")
        server_socket.close()

if __name__ == "__main__":
    main()