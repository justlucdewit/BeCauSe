instructions_map = {}

MEMORY_CAPACITY = 640_000

iota_counter = 0
def iota(name, reset=False):
    global iota_counter
    if reset:
        iota_counter = 0
    result = iota_counter
    iota_counter += 1

    instructions_map[result] = name

    return result

# Stack
OP_PUSH = iota("PUSH", True)
OP_DUP = iota("DUP")

# Math
OP_ADD = iota("ADD")
OP_SUBTRACT = iota("SUBTRACT")
OP_GREATER = iota("GREATER")
OP_SMALLER = iota("SMALLER")
OP_EQUAL = iota("EQUAL")

# Flow control
OP_IF = iota("IF")
OP_END = iota("END")
OP_ELSE = iota("ELSE")
OP_WHILE = iota("WHILE")
OP_DO = iota("DO")

# IO
OP_PRINT = iota("PRINT")

OP_MEM = iota("MEM")
OP_STORE = iota("STORE")
OP_LOAD = iota("LOAD")

# Non opcodes
NUMBER_OF_OPS = iota("NUM_OPS")