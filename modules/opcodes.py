iota_counter = 0
def iota(reset=False):
    global iota_counter
    if reset:
        iota_counter = 0
    result = iota_counter
    iota_counter += 1
    return result

# Stack
OP_PUSH = iota(True)
OP_DUP = iota()

# Math
OP_ADD = iota()
OP_SUBTRACT = iota()
OP_GREATER = iota()
OP_SMALLER = iota()
OP_EQUAL = iota()

# Flow control
OP_IF = iota()
OP_END = iota()
OP_ELSE = iota()
OP_WHILE = iota()
OP_DO = iota()

# IO
OP_PRINT = iota()

# Non opcodes
NUMBER_OF_OPS = iota()