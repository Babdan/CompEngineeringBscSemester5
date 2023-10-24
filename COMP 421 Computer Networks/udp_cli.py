import socket
import threading
import keyboard

def receive_messages(socket):
    while True:
        try:
            message, _ = socket.recvfrom(1024)
            message = message.decode('utf-8')
            print(message)
        except OSError as e:
            print(f"Error: {e}")
            break

def get_valid_port_input():
    while True:
        try:
            port = int(input("Enter a valid port number (1-65535): "))
            if 0 < port < 65536:
                return port
            else:
                print("Invalid port. Please enter a valid port number (1-65535).")
        except ValueError:
            print("Invalid input. Please enter a valid port number (1-65535).")

def get_valid_address_input():
    while True:
        address = input("Enter a valid address (e.g., localhost): ")
        if address:
            return address
        else:
            print("Invalid address. Please enter a valid address.")

def main():
    host = get_valid_address_input()
    port = get_valid_port_input()
    username = input("Enter your username: ")

    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind((host, port))

    # Start the receive thread
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    print("Press 'Ctrl + C' to exit.")

    try:
        while True:
            peer_host = host  # Use the same host as the destination
            peer_port = port  # Use the same port as the destination
            message = input("Enter your message: ")
            message = f"{username}: {message}"

            client_socket.sendto(message.encode('utf-8'), (peer_host, peer_port))
    except KeyboardInterrupt:
        print("\nExited. You can re-enter IP and port if needed.")

    # Close the socket when done
    client_socket.close()

if __name__ == "__main__":
    main()
