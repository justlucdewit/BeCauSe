from modules.opcodes import *

debug = False
stack = []
memory = bytearray(MEMORY_CAPACITY)

def run_program(program):
    ip = 0
    while ip < len(program):
        operation = program[ip]

        if operation[0] == OP_PUSH:
            stack.append(operation[1])

        elif operation[0] == OP_DUP:
            a = stack.pop()
            stack.append(a)
            stack.append(a)
        
        elif operation[0] == OP_2DUP:
            b = stack.pop()
            a = stack.pop()
            stack.append(a)
            stack.append(b)
            stack.append(a)
            stack.append(b)

        elif operation[0] == OP_DROP:
            stack.pop()

        elif operation[0] == OP_ADD:
            stack.append(stack.pop() + stack.pop())

        elif operation[0] == OP_SUBTRACT:
            a = stack.pop()
            b = stack.pop()
            stack.append(b - a)

        elif operation[0] == OP_SHIFT_LEFT:
            a = stack.pop()
            b = stack.pop()
            stack.append(int(b << a))

        elif operation[0] == OP_SHIFT_RIGHT:
            a = stack.pop()
            b = stack.pop()
            print(f"{b} >> {a} = {b >> a}")
            stack.append(int(b >> a))

        elif operation[0] == OP_BITWISE_AND:
            a = stack.pop()
            b = stack.pop()
            stack.append(int(b & a))

        elif operation[0] == OP_BITWISE_OR:
            a = stack.pop()
            b = stack.pop()
            stack.append(int(b | a))

        elif operation[0] == OP_PRINT:
            print(stack.pop())
        
        elif operation[0] == OP_GREATER:
            b = stack.pop()
            a = stack.pop()
            stack.append(int(a > b))

        elif operation[0] == OP_SMALLER:
            b = stack.pop()
            c = stack.pop()
            stack.append(int(a < b))

        elif operation[0] == OP_EQUAL:
            a = stack.pop()
            b = stack.pop()
            stack.append(int(a == b))

        elif operation[0] == OP_IF:
            a = stack.pop()
            if a == 0:
                ip = operation[1] - 1

        elif operation[0] == OP_ELSE:
            ip = operation[1] - 1

        elif operation[0] == OP_END:
            ip = operation[1] - 1

        elif operation[0] == OP_WHILE:
            pass

        elif operation[0] == OP_DO:
            a = stack.pop()

            if a == 0:
                ip = operation[1] - 1

        elif operation[0] == OP_MEM:
            stack.append(0)

        elif operation[0] == OP_LOAD:
            ptr = stack.pop()
            byte = memory[ptr] % 0xFF
            stack.append(byte)

        elif operation[0] == OP_STORE:
            byte = stack.pop()
            ptr = stack.pop()
            memory[ptr] = byte & 0xFF

        elif operation[0] == OP_SYSCALL0:
            syscall_num = stack.pop()
            emulate_unix(syscall_num, [])

        elif operation[0] == OP_SYSCALL1:
            syscall_num = stack.pop()
            emulate_unix(syscall_num, [stack.pop()])
    
        elif operation[0] == OP_SYSCALL2:
            syscall_num = stack.pop()
            emulate_unix(syscall_num, [stack.pop(), stack.pop()])

        elif operation[0] == OP_SYSCALL3:
            syscall_num = stack.pop()
            emulate_unix(syscall_num, [stack.pop(), stack.pop(), stack.pop()])

        elif operation[0] == OP_SYSCALL4:
            syscall_num = stack.pop()
            emulate_unix(syscall_num, [stack.pop(), stack.pop(), stack.pop(), stack.pop()])

        elif operation[0] == OP_SYSCALL5:
            syscall_num = stack.pop()
            emulate_unix(syscall_num, [stack.pop(), stack.pop(), stack.pop(), stack.pop(), stack.pop()])

        elif operation[0] == OP_SYSCALL6:
            syscall_num = stack.pop()
            emulate_unix(syscall_num, [stack.pop(), stack.pop(), stack.pop(), stack.pop(), stack.pop(), stack.pop()])

        else:
            print("Simulation Error: Unknown opcode encountered in run_program")
            exit(-1)

        ip += 1

def emulate_unix(syscall, values):
    # sys write
    if syscall == 1:
        if (len(values) < 3):
            unix_emulation_error(3, len(values))

        # write to std out
        if (values[0] == 1):
            for byte in memory[values[1]:values[1]+values[2]]:
                print(chr(byte), end="")
        

    # sys exit
    elif syscall == 60:
        if (len(values) < 1):
            unix_emulation_error(1, len(values))
        exit(values[0])

    

def unix_emulation_error(expected_count, received_count):
    print(f"Simulation Error: expected at least {expected_count} values for syscall, got {received_count} values")
    exit(-1)
