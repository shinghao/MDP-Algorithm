import Constants

UNIT_D = 10
UNIT_T = 90


def map_control(instr, rep):
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
        return "nq0%s" % (UNIT_T)

    elif instr == 'right':
        return "ne0%s" % (UNIT_T)

    elif instr == 'backleft':
        return "nz0%s" % (UNIT_T)

    elif instr == 'backright':
        return "nc0%s" % (UNIT_T)

    else:
        raise Exception(
            "Invalid Instr type. Check instruction formatting before translating")


def translate(instr_list):
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


def translate_instructions_to_RPI(instr_list):
    result = ''
    for instr_to_obstacle in instr_list:
        result += ','.join(str(instr) for instr in instr_to_obstacle)
        result += ':'
    return result[:-1]  # remove last comma


def translate_obstacles_from_RPI(obstacle_str: str):
    directions = {'N': Constants.N, 'S': Constants.S,
                  'E': Constants.E, 'W': Constants.W}

    result = []
    obstacle_list = obstacle_str.split(',')
    for obstacle in obstacle_list:
        x, y = (int)(obstacle[:2]), (int)(obstacle[2:4])

        if obstacle[4] in directions:
            direc = directions[obstacle[4]]
        else:
            print("Incorrect direction format")

        result.append((x, y, direc))

    return result


if __name__ == '__main__':
    example = ['forward', 'back', 'back', 'right',
               'right', 'left', 'forward', 'forward', 'forward']
    print(translate(example))
