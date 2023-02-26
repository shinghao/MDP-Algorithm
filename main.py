import socket
from PathGenerator import PathGenerator
import mapping
from griddyworld import *


def check_round_obstacle():
    '''
    Generate a pre-determined string of instruction that will enable robot to navigate to other 3 faces of the obstacle
    Requires the robot to already be facing and near a face of the obstacle
    Return: String
    '''
    instruction_list = "nq090,nx030,nc045,nx005,nz040:" * 3
    return instruction_list[:-1]


def generate_translated_instruction(obstacle_str):
    '''
    Input: obstacle_str (str) message from RPI

    1. Translate obstacle_string from RPI message format to list of tuples
    2. Create PathGenerator object and generate entire algo path
    3. Get list of instructions from PathGenerator
    4. Translate instruction list from tuple to RPI format. Store result in translated_instr_list
    5. Convert list translated instructions into a single string for sending back to RPI

    Return: instruction_str (str) message for RPI
    '''
    # Translate obstacle_string from RPI message format to list of tuples
    obstacle_list = mapping.translate_obstacles_from_RPI(obstacle_str)

    # Create PathGenerator object and generate entire algo path
    path_generator = PathGenerator()
    path_generator.generate_path(obstacle_list, is_sim=False)

    # Get list of obstacles in order of visitation
    obstacles_ordered = path_generator.get_obstacles_ordered()

    # Get list of instructions from PathGenerator
    instr_list = path_generator.get_instruction_list()

    # Translate instruction list from tuple to RPI format. Store result in translated_instr_list
    translated_instr_list = []
    for instr in instr_list:
        translated_instr_list.append(
            mapping.translate(instr.get_moves()))

    # Convert list translated instructions into a single string for sending back to RPI
    instruction_str = mapping.translate_instructions_to_RPI(
        translated_instr_list)

    # Return single instruction string
    return instruction_str


def main():
    # Define the address and port to listen on
    port = 6969  # Choose a port number

    # Create a TCP/IP socket and bind it to the address and port
    # sock = socket.socket()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind(('', port))

    # Listen for incoming connections
    sock.listen(5)
    print(f'Listening on {port}...')
    conn, addr = sock.accept()
    while True:
        # Wait for a connection
        print(f'Connected by {addr}')

        # Receive data from the client
        data = conn.recv(1024)
        if not data:
            break
        message = data.decode()
        print(f'Received "{message}" from {addr}')

        # A5 - UNCOMMENT THIS ONLY FOR A5
        # instruction_message = check_round_obstacle()

        # Translate obstacle string, start pathfinding, generate instructions and translate instr_list string to send to RPI
        instruction_message = generate_translated_instruction(message)

        # Send a response to the client
        print("sending...", instruction_message)

        response = instruction_message
        conn.sendall(response.encode())

    conn.close()
    sock.close()

    # Clean up the connection

    # test = (go_round_obstacle("n10101W"))
    # print(check_round_obstacle())


if __name__ == "__main__":
    main()
