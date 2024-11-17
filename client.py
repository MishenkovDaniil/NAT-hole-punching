import socket
import time
import threading

RENDEZVOUS_IP = "192.168.0.2"  
RENDEZVOUS_PORT = 5000         
LOCAL_PORT = 4000                      
HOLE_PUNCH_MAX_TRY = 5

def listen_for_messages(client_socket):
    while True:
        try:
            data, addr = client_socket.recvfrom(1024)
            print(f"Received message from {addr}: {data.decode()}")
        except Exception as err:
            print(f"Error while receiving msg {err}")
            break

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #udp
    
    client_socket.bind(("0.0.0.0", LOCAL_PORT))

    message = "Hello"
    
    client_socket.sendto(message.encode(), (RENDEZVOUS_IP, RENDEZVOUS_PORT))
    print(f"Sent msg to server: {RENDEZVOUS_IP}:{RENDEZVOUS_PORT}")

    data, server_addr = client_socket.recvfrom(1024)
    print(f"peer info: {data.decode()}")
    
    peer_ip, peer_port = data.decode().split(":")
    peer_port = int(peer_port)

    print(f"Peer: {peer_ip}:{peer_port}")
    
    listener_thread = threading.Thread(target=listen_for_messages, args=(client_socket,))
    listener_thread.daemon = True
    listener_thread.start()

    for i in range (HOLE_PUNCH_MAX_TRY):  
        client_socket.sendto("Punch".encode(), (peer_ip, peer_port))
        print(f"Sending NAT punch to {peer_ip}:{peer_port}")
        time.sleep(1)

    while True:
        message = input("Enter message: ")
        client_socket.sendto(message.encode(), (peer_ip, peer_port))

if __name__ == "__main__":
    main()