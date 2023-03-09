import Constants

UNIT_D = 10
UNIT_T_L = 87
UNIT_T_R = 88
CALIBRATION = 3


def map_control(instr, rep):
    '''
    Translate instruction (instr) to commands for the RPI.
    '''
    if instr == 'forward':
        if rep < 10:
            return "nw0%s" % (UNIT_D*rep)
        else:
            return "nw%s" % (UNIT_D*rep)

    elif instr == 'back':
        if rep < 10:
            return "nx0%s" % (UNIT_D*rep)
        else:
            return "nx%s" % (UNIT_D*rep)

    elif instr == 'left':
        return "nq0%s,nw00%s" % (UNIT_T_L, CALIBRATION)

    elif instr == 'right':
        # return "ne0%s,nw00%s" % (UNIT_T_R, CALIBRATION)
        return "ne043,nx015,ne043,nw003"  # hardcoded

    elif instr == 'backleft':
        return "nx00%s,nz0%s" % (CALIBRATION, UNIT_T_L)

    elif instr == 'backright':
        # return "nx00%s,nc0%s" % (CALIBRATION, UNIT_T_R)
        return "nx003,nc043,nw015,nc043"  # hardcoded

    else:
        raise Exception(
            "Invalid Instruction type. Check instruction formatting before translating")


def translate(instr_list):
    '''
    Take input a list of instructions and translate each instruction to RPI commands by calling map_control() function
    '''
    final_instr = list()
    last = instr_list[0]
    count = 1

    for i in instr_list[1:]:
        if i == last and (i == 'forward' or i == 'back'):
            count += 1
        else:
            final_instr.append(map_control(last, count))
            count = 1
            last = i

    if i == last:
        final_instr.append(map_control(last, count))
        count = 1
        last = i

    return final_instr


# format - "nq010,nw010:nq010,nw010" - instruction seperated by "," and each path to an obstacle seperated by ":"
def translate_instructions_to_RPI(instr_list):
    '''
    Convert entire list of instruction to string format for RPI
    Input: List of instructions already translated to RPI format
    Return: String
    '''
    result = ''
    for instr_to_obstacle in instr_list:
        result += ','.join(str(instr) for instr in instr_to_obstacle)
        result += ':'
    return result[:-1]  # remove last comma


# format - "nXXYYiN,nXXYYiN" -> Obstacles from RPI to obstacles object
def translate_obstacles_from_RPI(obstacle_str: str):
    '''
    Translate obstacles from RPI string format to a list of (id, x, y, direction) tuples
    '''
    directions = {'N': Constants.N, 'S': Constants.S,
                  'E': Constants.E, 'W': Constants.W}

    result = []
    obstacle_list = obstacle_str.split(',')
    for obstacle in obstacle_list:
        x, y = (int)(obstacle[1:3]), (int)(obstacle[3:5])
        id = obstacle[5]
        if obstacle[6] in directions:
            direc = directions[obstacle[6]]
        else:
            print("Error: Incorrect obstacle format - Direction not N, S, E, W")
        result.append((id, x, y, direc))

    return result

# number_of_positions_sent, item_not_doing, item_not_doing, item_not_doing, original (order, and insturctions)


def translate_obstacles_to_RPI(obstacle_obj_list: list, obstacle_list_initial: list):
    directions = {'N': Constants.N, 'S': Constants.S,
                  'E': Constants.E, 'W': Constants.W}

    result_str = ""
    result_str += str(len(obstacle_obj_list)) + ","

    for i in range(len(obstacle_list_initial)):
        obstacle_list_initial[i] = int(obstacle_list_initial[i][0])

    result_list = []

    for obs in obstacle_obj_list:
        result_list.append(int(obs.ID))

    if (len(obstacle_obj_list) != len(obstacle_list_initial)):
        for obsID in obstacle_list_initial:
            if obsID not in result_list:
                result_str += str(obsID) + ","

    for obsID in result_list:
        result_str += str(obsID) + ","

    return result_str
