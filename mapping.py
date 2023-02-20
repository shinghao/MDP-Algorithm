UNIT_D = 10
UNIT_T = 90

def map_control(instr, rep):
	if instr == 'forward':
		if rep < 10: return "nw0%s" %(UNIT_D*rep)
		else: return "nw%s" %(UNIT_D*rep)

	elif instr == 'back':
		if rep < 10: return "nx0%s" %(UNIT_D*rep)
		else: return "nx%s" %(UNIT_D*rep)

	elif instr == 'left':
		return "nq0%s" %(UNIT_T)

	elif instr == 'right':
		return "ne0%s" %(UNIT_T)

	elif instr == 'backleft':
		return "nz0%s" %(UNIT_T)

	elif instr == 'backright':
		return "nc0%s" %(UNIT_T)

	else: raise Exception("Invalid Instr type. Check instruction formatting before translating")



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


# def translate(instr, controls = robot.controls()):
# 	#qwezxc
# 	if instr == 'forward':
# 		return "nw"

if __name__ == '__main__':
	example = ['forward','back','back','right', 'right', 'left','forward','forward','forward']
	print(translate(example))