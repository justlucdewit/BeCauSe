iota_counter = 0
def iota(reset=False):
    global iota_counter
    if reset:
        iota_counter = 0
    result = iota_counter
    iota_counter += 1
    return result

OP_PUSH = iota(True)
OP_ADD = iota()
OP_SUBTRACT = iota()
OP_PRINT = iota()
NUMBER_OF_OPS = iota()