from modules.opcodes import *

def run_program(program):
    stack = []
    for operation in program:
        if operation[0] == OP_PUSH:
            stack.append(operation[1])
        elif operation[0] == OP_ADD:
            stack.append(stack.pop() + stack.pop())
        elif operation[0] == OP_SUBTRACT:
            a = stack.pop()
            b = stack.pop()
            stack.append(b - a)
        elif operation[0] == OP_PRINT:
            print(stack.pop())
        else:
            assert False, "Unknown opcode"