instructions_map = {}
scoped_instructions = []

MEMORY_CAPACITY = 640_000
STRING_CAPACITY = 640_000

iota_counter = 0


def register_operation(name, scoped=False):
    global iota_counter
    result = iota_counter
    iota_counter += 1

    instructions_map[result] = name

    if scoped:
        scoped_instructions.append(result)

    return result


class Operation:
    # Stack
    PUSH_INT = register_operation("PUSH")
    PUSH_STRING = register_operation("PUSH")
    DUP = register_operation("DUP")
    TWO_DUP = register_operation("2DUP")
    DROP = register_operation("DROP")
    TWO_DROP = register_operation("2DROP")
    SWAP = register_operation("SWAP")
    OVER = register_operation("OVER")
    ROT = register_operation("ROT")

    # Math
    ADD = register_operation("ADD")
    SUBTRACT = register_operation("SUBTRACT")
    MULTIPLY = register_operation("MULTIPLY")
    GREATER = register_operation("GREATER")
    SMALLER = register_operation("SMALLER")
    EQUAL = register_operation("EQUAL")
    SHIFT_LEFT = register_operation("BITWISE LEFTSHIFT")
    SHIFT_RIGHT = register_operation("BITWISE RIGHTSHIFT")
    BITWISE_AND = register_operation("BITWISE AND")
    BITWISE_OR = register_operation("BITWISE OR")
    MODULE = register_operation("MODULATION")
    GREATER_EQUAL = register_operation("GREATER_EQUAL")
    SMALLER_EQUAL = register_operation("SMALLER_EQUAL")

    # IO
    PRINT = register_operation("PRINT")
    SYSCALL0 = register_operation("SYSCALL0")
    SYSCALL1 = register_operation("SYSCALL1")
    SYSCALL2 = register_operation("SYSCALL2")
    SYSCALL3 = register_operation("SYSCALL3")
    SYSCALL4 = register_operation("SYSCALL4")
    SYSCALL5 = register_operation("SYSCALL5")
    SYSCALL6 = register_operation("SYSCALL6")

    # Memory
    MEM = register_operation("MEM")
    STORE8 = register_operation("STORE8")
    STORE16 = register_operation("STORE16")
    STORE32 = register_operation("STORE32")
    STORE64 = register_operation("STORE64")
    LOAD8 = register_operation("LOAD8")
    LOAD16 = register_operation("LOAD16")
    LOAD32 = register_operation("LOAD32")
    LOAD64 = register_operation("LOAD64")

    # Other
    HERE = register_operation("HERE")


class Keyword:
    IF = register_operation("IF", scoped=True)
    END = register_operation("END")
    ELSE = register_operation("ELSE")
    WHILE = register_operation("WHILE")
    DO = register_operation("DO", scoped=True)
    MACRO = register_operation("MACRO", scoped=True)
    CONST = register_operation("CONST")
    ENUM = register_operation("ENUM", scoped=True)
    IMPORT = register_operation("IMPORT")
    MEMORY = register_operation("MEMORY", scoped=True)


class TokenType:
    INT = register_operation("INT")
    WORD = register_operation("WORD")
    STRING = register_operation("STRING")
    CHAR = register_operation("CHARACTER")


# Non opcodes
NUMBER_OF_OPS = register_operation("NUM_OPS")
