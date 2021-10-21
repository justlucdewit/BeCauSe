from modules.opcodes import *

debug = False

def debug_print(*msg):
    if debug:
        print(*msg)

def run_program(program):
    stack = []
    ip = 0
    debug_print(program)
    while ip < len(program):
        operation = program[ip]

        if operation[0] == OP_PUSH:
            debug_print(ip, "PUSH ", operation[1])
            stack.append(operation[1])

        elif operation[0] == OP_DUP:
            debug_print(ip, "DUP")
            a = stack.pop()
            stack.append(a)
            stack.append(a)

        elif operation[0] == OP_ADD:
            debug_print(ip, "ADD")
            stack.append(stack.pop() + stack.pop())

        elif operation[0] == OP_SUBTRACT:
            debug_print(ip, "SUBT")
            a = stack.pop()
            b = stack.pop()
            stack.append(b - a)

        elif operation[0] == OP_PRINT:
            debug_print(ip, "PRINT")
            print(stack.pop())
        
        elif operation[0] == OP_GREATER:
            debug_print(ip, "GREATER")
            b = stack.pop()
            a = stack.pop()
            stack.append(int(a > b))

        elif operation[0] == OP_SMALLER:
            debug_print(ip, "SMALLER")
            b = stack.pop()
            c = stack.pop()
            stack.append(int(a < b))

        elif operation[0] == OP_EQUAL:
            debug_print(ip, "EQ")
            a = stack.pop()
            b = stack.pop()
            stack.append(int(a == b))

        elif operation[0] == OP_IF:
            debug_print(ip, "IF")
            a = stack.pop()
            if a == 0:
                ip = operation[1] - 1

        elif operation[0] == OP_ELSE:
            debug_print(ip, "ELSE ", operation[1])
            ip = operation[1]

        elif operation[0] == OP_END:
            debug_print(ip, "END")
            ip = operation[1]

        elif operation[0] == OP_WHILE:
            pass

        elif operation[0] == OP_DO:
            a = stack.pop()

            if a == 0:
                ip = operation[1]


        else:
            print("Error: Unknown opcode encountered in run_program")
            exit(-1)

        ip += 1