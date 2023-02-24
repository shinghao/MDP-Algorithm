import socket
from PathGenerator import PathGenerator
import mapping
from griddyworld import *


def go_round_obstacle(obstacle):
    x, y = (obstacle[1:3]), (obstacle[3:5])

    directions = ['N', 'S', 'E', 'W']
    index_pos = directions.index(obstacle[6])
    new_directions = directions[index_pos:] + directions[:index_pos]

    print(new_directions)
    target_pos = ""

    for d in new_directions:
        target_pos += ("n" + x + y + d + ",")

    return target_pos[:-1]

# "nq090,nx030,nc045,nx015,nz040,nw010:"


def check_round_obstacle():
    instruction_list = "nq090,nx030,nc045,nx005,nz040:" * 3
    return instruction_list[:-1]


def generate_translated_instruction(obstacle_list):

    # Generate path using algo
    path_generator = PathGenerator()
    path_generator.generate_path(obstacle_list, is_sim=False)

    # Get list of obstacles in order of visitation
    obstacles_ordered = path_generator.get_obstacles_ordered()

    # Get list of instructions
    instruction_list = path_generator.get_instruction_list()

    # Translate instruction list to RPI format
    translated_instruction_list = []
    for instructions in instruction_list:
        translated_instruction_list.append(
            mapping.translate(instructions.get_moves()))

    # Translate instruction list to instruction string
    instruction_str = mapping.translate_instructions_to_RPI(
        translated_instruction_list)
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

        instruction_message = check_round_obstacle()
        # else:
        #     # Translate obstacles mnessage from string to list
        #     obstacle_list = mapping.translate_obstacles_from_RPI(
        #         message)

        #     # Start pathfinding, generate instructions and translate to string to send to RPI
        #     instruction_message = generate_translated_instruction(
        #         obstacle_list)

        # Send a response to the client
        print("sending...", instruction_message)

        response = instruction_message
        conn.sendall(response.encode())

    conn.close()
    sock.close()

    # Clean up the connection

    # test = (go_round_obstacle("n10101W"))
    # print(check_round_obstacle())


# if __name__ == "__main__":
    # main()
