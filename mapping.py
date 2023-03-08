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
        return "nx003 nc043 nw015 nc043"  # hardcoded

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


# format - "nXXYYiN,nXXYYiN"
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


def translate_obstacles_to_RPI(obstacle_list: list):
    directions = {'N': Constants.N, 'S': Constants.S,
                  'E': Constants.E, 'W': Constants.W}

    result = ""
    for obs in obstacle_list:
        result += obs.ID + ","

    return result
