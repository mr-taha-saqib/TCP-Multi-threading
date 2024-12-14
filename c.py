import socket

def run_client():
    # Create a socket for communication
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 9000))  # Connect to the server on localhost at port 9000

    while True:
        server_message = client_socket.recv(4096).decode()  # Receive message from the server
        print(server_message)  # Display the server's message
        
        if "Please enter your Name/CNIC:" in server_message:
            voter_details = input("Enter your Name/CNIC: ")
            client_socket.send(voter_details.encode())
        
        elif "Please cast your vote by entering the poll symbol:" in server_message:
            vote_symbol = input("Enter your vote (poll symbol): ")  # Get the user's vote
            client_socket.send(vote_symbol.encode())
            break  # Exit loop after sending the vote

    print(client_socket.recv(4096).decode())  # Receive and display final thank you message
    client_socket.close()  # Close the connection

if __name__ == "__main__":
    run_client()