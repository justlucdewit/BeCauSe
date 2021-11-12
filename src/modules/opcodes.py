instructions_map = {}

MEMORY_CAPACITY = 640_000
STRING_CAPACITY = 640_000

iota_counter = 0


def register_operation(name, reset=False):
    global iota_counter
    if reset:
        iota_counter = 0
    result = iota_counter
    iota_counter += 1

    instructions_map[result] = name

    return result


# Stack
OP_PUSH = register_operation("PUSH", True)
OP_PUSH_STRING = register_operation("PUSH")
OP_DUP = register_operation("DUP")
OP_2DUP = register_operation("2DUP")
OP_DROP = register_operation("DROP")
OP_SWAP = register_operation("SWAP")
OP_OVER = register_operation("OVER")

# Math
OP_ADD = register_operation("ADD")
OP_SUBTRACT = register_operation("SUBTRACT")
OP_MULTIPLY = register_operation("MULTIPLY")
OP_GREATER = register_operation("GREATER")
OP_SMALLER = register_operation("SMALLER")
OP_EQUAL = register_operation("EQUAL")
OP_SHIFT_LEFT = register_operation("BITWISE LEFTSHIFT")
OP_SHIFT_RIGHT = register_operation("BITWISE RIGHTSHIFT")
OP_BITWISE_AND = register_operation("BITWISE AND")
OP_BITWISE_OR = register_operation("BITWISE OR")

# Flow control
OP_IF = register_operation("IF")
OP_END = register_operation("END")
OP_ELSE = register_operation("ELSE")
OP_WHILE = register_operation("WHILE")
OP_DO = register_operation("DO")
OP_MACRO = register_operation("MACRO")

# IO
OP_PRINT = register_operation("PRINT")
OP_SYSCALL0 = register_operation("SYSCALL0")
OP_SYSCALL1 = register_operation("SYSCALL1")
OP_SYSCALL2 = register_operation("SYSCALL2")
OP_SYSCALL3 = register_operation("SYSCALL3")
OP_SYSCALL4 = register_operation("SYSCALL4")
OP_SYSCALL5 = register_operation("SYSCALL5")
OP_SYSCALL6 = register_operation("SYSCALL6")

# Memory
OP_MEM = register_operation("MEM")
OP_STORE = register_operation("STORE")
OP_LOAD = register_operation("LOAD")

# Other
OP_IMPORT = register_operation("IMPORT")

# Token types
TOK_INT = register_operation("INT")
TOK_WORD = register_operation("WORD")
TOK_STRING = register_operation("STRING")
TOK_CHAR = register_operation("CHARACTER")

# Non opcodes
NUMBER_OF_OPS = register_operation("NUM_OPS")
