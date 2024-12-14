import socket  # TCP/IP
import threading

def read_voter_data():
    voter_data = {}
    with open('Voters_List.txt', 'r') as voter_file:
        for entry in voter_file:
            name, cnic = entry.strip().split('/')  # Split name and CNIC
            voter_data[name] = cnic.strip()
    return voter_data

def read_candidate_data():
    candidate_list = []
    with open('Candidates_List.txt', 'r') as candidate_file:
        for entry in candidate_file:
            candidate_list.append(entry.strip())  # Clean each candidate's name
    return candidate_list

def process_client_connection(client_socket, voter_data, candidate_list):
    try:
        # Prompting for voter's Name/CNIC
        client_socket.send(b"Please enter your Name/CNIC: ")
        voter_input = client_socket.recv(1024).decode().strip()
        
        # Authenticate voter
        name, cnic = voter_input.split('/')
        if name in voter_data and voter_data[name] == cnic:
            client_socket.send(b"Authentication successful! Here are the candidates:\n")
            for candidate in candidate_list:
                client_socket.send(f"{candidate}\n".encode())
            client_socket.send(b"Please cast your vote by entering the poll symbol: ")

            vote_choice = client_socket.recv(1024).decode().strip()
            log_vote(name, vote_choice)
            client_socket.send(b"Your vote has been recorded. Thank you!\n")
        else:
            client_socket.send(b"Authentication failed. Voting is not allowed.\n")
    finally:
        client_socket.close()

def log_vote(voter_name, vote_choice):
    with open('Output.txt', 'a') as output_file:
        output_file.write(f"{voter_name} voted for {vote_choice}\n")

def initialize_server():
    voter_data = read_voter_data()
    candidate_list = read_candidate_data()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 9000))
    server_socket.listen(5) # binds
    print("Server is running and listening on port 9000 ...")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection established with {address}")
        threading.Thread(target=process_client_connection, args=(client_socket, voter_data, candidate_list)).start()

if __name__ == "__main__":
    initialize_server()