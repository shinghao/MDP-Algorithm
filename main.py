from mapping import map_control
from PathGenerator import PathGenerator
import mapping
from griddyworld import *
import Constants


def main():
    # Receive obstacle_list from RPI
    obstacles = "0608N,1414N"
    obstacles = mapping.translate_obstacles_from_RPI(obstacles)
    print("Translated obstacles: ", obstacles)
    # Generate path
    path_generator = PathGenerator()
    path_generator.generate_path(obstacles, is_sim=False)

    # List of obstacles in order of visitation
    obstacles_ordered = path_generator.get_obstacles_ordered()

    # List of instructions
    instruction_list = path_generator.get_instruction_list()

    # Translate instructions to RPI format
    translated_instruction_list = []
    for instructions in instruction_list:
        translated_instruction_list.append(
            mapping.translate(instructions.get_moves()))
    instruction_str = mapping.translate_instructions_to_RPI(
        translated_instruction_list)
    print(translated_instruction_list)
    print("STRING INSTRUCTIONS FOR RPI: ", instruction_str)


if __name__ == "__main__":
    main()
