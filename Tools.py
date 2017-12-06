import msvcrt

#判断end是否小于0
def end_less_than_0(node):
    if node.end < 0:
        return True
    else:
        return False


#判断end是否小于0
def end_less_than_0_and_not_initializtion(node):
    if len(node.label) == 1:
        return False
    if node.end < 0:
        return True
    else:
        return False

def end_program():
    print("Press 'D' to exit...")

    while True:
        if ord(msvcrt.getch()) in [68, 100]:
            break