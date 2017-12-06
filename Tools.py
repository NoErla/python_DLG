import msvcrt


'''
#判断end是否小于0
def end_less_than_0(node):
    if node.end < 0:
        return True
    else:
        return False
'''


#判断end是否小于0
def end_less_than_0_and_can_merge(node):
    if len(node.label) == 1:
        return False
    for in_neighbour in node.in_neighbours:
        if len(in_neighbour.label) > len(node.label):
            return False
    for out_neighbour in node.out_neighbours:
        if len(out_neighbour.label) > len(node.label):
            return False
    return True

def end_program():
    print("Press 'D' to exit...")

    while True:
        if ord(msvcrt.getch()) in [68, 100]:
            break