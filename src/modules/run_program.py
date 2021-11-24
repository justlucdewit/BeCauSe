from modules.opcodes import (MEMORY_CAPACITY, OP_2DUP, OP_ADD, OP_BITWISE_AND,
                             OP_BITWISE_OR, OP_DO, OP_DROP, OP_DUP, OP_ELSE,
                             OP_END, OP_EQUAL, OP_GREATER, OP_IF, OP_LOAD,
                             OP_MEM, OP_MULTIPLY, OP_OVER, OP_PRINT,
                             OP_PUSH_STRING, OP_SHIFT_LEFT, OP_SHIFT_RIGHT,
                             OP_SMALLER, OP_STORE, OP_SUBTRACT, OP_SWAP,
                             OP_SYSCALL0, OP_SYSCALL1, OP_SYSCALL2,
                             OP_SYSCALL3, OP_SYSCALL4, OP_SYSCALL5,
                             OP_SYSCALL6, OP_WHILE, STRING_CAPACITY, OP_PUSH,
                             OP_STORE64, OP_STORE32, OP_LOAD16, OP_LOAD32,
                             OP_LOAD64, OP_LOAD8, OP_STORE16, OP_STORE8)

debug = False
stack = []
memory = bytearray(MEMORY_CAPACITY + STRING_CAPACITY)


def run_program(program):
    ip = 0
    str_size = 0

    while ip < len(program):
        operation = program[ip]

        if operation['type'] == OP_PUSH:
            stack.append(operation['value'])

        elif operation['type'] == OP_PUSH_STRING:
            bs = bytes(operation['value'], 'utf-8')
            n = len(bs)
            stack.append(n)
            if 'addr' not in operation:
                memory[str_size:str_size +
                       n] = bs
                operation['addr'] = str_size
                str_size += n

            stack.append(operation['addr'])

        elif operation['type'] == OP_DUP:
            a = stack.pop()
            stack.append(a)
            stack.append(a)

        elif operation['type'] == OP_2DUP:
            b = stack.pop()
            a = stack.pop()
            stack.append(a)
            stack.append(b)
            stack.append(a)
            stack.append(b)

        elif operation['type'] == OP_DROP:
            stack.pop()

        elif operation['type'] == OP_SWAP:
            a = stack.pop()
            b = stack.pop()
            stack.append(a)
            stack.append(b)

        elif operation['type'] == OP_OVER:
            a = stack.pop()
            b = stack.pop()
            stack.append(b)
            stack.append(a)
            stack.append(b)

        elif operation['type'] == OP_ADD:
            stack.append(stack.pop() + stack.pop())

        elif operation['type'] == OP_SUBTRACT:
            a = stack.pop()
            b = stack.pop()
            stack.append(b - a)

        elif operation['type'] == OP_MULTIPLY:
            a = stack.pop()
            b = stack.pop()
            stack.append(b * a)

        elif operation['type'] == OP_SHIFT_LEFT:
            a = stack.pop()
            b = stack.pop()
            stack.append(int(b << a))

        elif operation['type'] == OP_SHIFT_RIGHT:
            a = stack.pop()
            b = stack.pop()
            stack.append(int(b >> a))

        elif operation['type'] == OP_BITWISE_AND:
            a = stack.pop()
            b = stack.pop()
            stack.append(int(b & a))

        elif operation['type'] == OP_BITWISE_OR:
            a = stack.pop()
            b = stack.pop()
            stack.append(int(b | a))

        elif operation['type'] == OP_PRINT:
            print(stack.pop())

        elif operation['type'] == OP_GREATER:
            a = stack.pop()
            b = stack.pop()
            stack.append(int(b > a))

        elif operation['type'] == OP_SMALLER:
            a = stack.pop()
            b = stack.pop()
            stack.append(int(b < a))

        elif operation['type'] == OP_EQUAL:
            a = stack.pop()
            b = stack.pop()
            stack.append(int(a == b))

        elif operation['type'] == OP_IF:
            a = stack.pop()
            if a == 0:
                ip = operation['reference'] - 1

        elif operation['type'] == OP_ELSE:
            ip = operation['reference'] - 1

        elif operation['type'] == OP_END:
            ip = operation['reference'] - 1

        elif operation['type'] == OP_WHILE:
            pass

        elif operation['type'] == OP_DO:
            a = stack.pop()

            if a == 0:
                ip = operation['reference'] - 1

        elif operation['type'] == OP_MEM:
            stack.append(STRING_CAPACITY)

        elif operation['type'] == OP_LOAD8:
            address = stack.pop()
            byte = memory[address] % 0xFF
            stack.append(byte)

        elif operation['type'] == OP_LOAD16:
            address = stack.pop()
            value = int.from_bytes(
                memory[address:address+2],
                byteorder="little")
            stack.append(value)

        elif operation['type'] == OP_LOAD32:
            address = stack.pop()
            value = int.from_bytes(
                memory[address:address+4],
                byteorder="little")
            stack.append(value)

        elif operation['type'] == OP_LOAD64:
            address = stack.pop()
            value = int.from_bytes(
                memory[address:address+8],
                byteorder="little")
            stack.append(value)

        elif operation['type'] == OP_STORE8:
            address = stack.pop()
            value = stack.pop()
            memory[address] = value & 0xFF

        elif operation['type'] == OP_STORE16:
            address = stack.pop()
            value = stack.pop()
            memory[address:address + 2] = value.to_bytes(
                length=2,
                byteorder="little",
                signed=(value < 0))

        elif operation['type'] == OP_STORE32:
            address = stack.pop()
            value = stack.pop()
            memory[address:address + 4] = value.to_bytes(
                length=4,
                byteorder="little",
                signed=(value < 0))

        elif operation['type'] == OP_STORE64:
            address = stack.pop()
            value = stack.pop()
            memory[address:address + 8] = value.to_bytes(
                length=8,
                byteorder="little",
                signed=(value < 0))
            print(memory[address])

        elif operation['type'] == OP_SYSCALL0:
            syscall_num = stack.pop()
            emulate_unix(syscall_num, [])

        elif operation['type'] == OP_SYSCALL1:
            syscall_num = stack.pop()
            emulate_unix(syscall_num, [stack.pop()])

        elif operation['type'] == OP_SYSCALL2:
            syscall_num = stack.pop()
            emulate_unix(syscall_num, [stack.pop(), stack.pop()])

        elif operation['type'] == OP_SYSCALL3:
            syscall_num = stack.pop()
            emulate_unix(syscall_num, [stack.pop(), stack.pop(), stack.pop()])

        elif operation['type'] == OP_SYSCALL4:
            syscall_num = stack.pop()
            emulate_unix(syscall_num, [stack.pop(),
                                       stack.pop(), stack.pop(), stack.pop()])

        elif operation['type'] == OP_SYSCALL5:
            syscall_num = stack.pop()
            emulate_unix(syscall_num, [stack.pop(), stack.pop(
            ), stack.pop(), stack.pop(), stack.pop()])

        elif operation['type'] == OP_SYSCALL6:
            syscall_num = stack.pop()
            emulate_unix(syscall_num, [stack.pop(), stack.pop(
            ), stack.pop(), stack.pop(), stack.pop(), stack.pop()])

        else:
            print(
                "Simulation Error: Unknown opcode "
                "encountered in run_program")
            exit(-1)

        ip += 1


def emulate_unix(syscall, values):
    # sys read
    if syscall == 0:
        if len(values) < 3:
            unix_emulation_error(3, len(values))

        # read from stdin
        if values[0] == 0:
            user_input = input() + "\n"
            i = 0

            if len(user_input) < values[2]:
                user_input += "\0" * (values[2] - len(user_input))

            for i in range(values[2]):
                memory[values[1] + i] = ord(user_input[i])

    # sys write
    elif syscall == 1:
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
    print(
        f"Simulation Error: expected at least {expected_count} values for "
        "syscall, got {received_count} values")
    exit(-1)
