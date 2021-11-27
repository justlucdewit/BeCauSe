from modules.opcodes import MEMORY_CAPACITY, STRING_CAPACITY, Operation, Keyword

debug = False
stack = []
memory = bytearray(MEMORY_CAPACITY + STRING_CAPACITY)


def run_program(program):
    ip = 0
    str_size = 0

    while ip < len(program):
        operation = program[ip]

        if operation['type'] == Operation.PUSH:
            stack.append(operation['value'])

        elif operation['type'] == Operation.PUSH_STRING:
            bs = bytes(operation['value'], 'utf-8')
            n = len(bs)
            stack.append(n)
            if 'addr' not in operation:
                memory[str_size:str_size +
                       n] = bs
                operation['addr'] = str_size
                str_size += n

            stack.append(operation['addr'])

        elif operation['type'] == Operation.DUP:
            a = stack.pop()
            stack.append(a)
            stack.append(a)

        elif operation['type'] == Operation.TWODUP:
            b = stack.pop()
            a = stack.pop()
            stack.append(a)
            stack.append(b)
            stack.append(a)
            stack.append(b)

        elif operation['type'] == Operation.DROP:
            stack.pop()

        elif operation['type'] == Operation.TWODROP:
            stack.pop()
            stack.pop()
            
        elif operation['type'] == Operation.SWAP:
            a = stack.pop()
            b = stack.pop()
            stack.append(a)
            stack.append(b)

        elif operation['type'] == Operation.OVER:
            a = stack.pop()
            b = stack.pop()
            stack.append(b)
            stack.append(a)
            stack.append(b)

        elif operation['type'] == Operation.ROT:
            a = stack.pop()
            b = stack.pop()
            c = stack.pop()
            stack.append(b)
            stack.append(a)
            stack.append(c)

        elif operation['type'] == Operation.ADD:
            stack.append(stack.pop() + stack.pop())

        elif operation['type'] == Operation.SUBTRACT:
            a = stack.pop()
            b = stack.pop()
            res = b - a
            if res < 0:
                res = 0xFFFFFFFFFFFFFFFF + res + 1
            stack.append(res)

        elif operation['type'] == Operation.MULTIPLY:
            a = stack.pop()
            b = stack.pop()
            stack.append(b * a)

        elif operation['type'] == Operation.SHIFT_LEFT:
            a = stack.pop()
            b = stack.pop()
            stack.append(int(b << a))

        elif operation['type'] == Operation.SHIFT_RIGHT:
            a = stack.pop()
            b = stack.pop()
            stack.append(int(b >> a))

        elif operation['type'] == Operation.BITWISE_AND:
            a = stack.pop()
            b = stack.pop()
            stack.append(int(b & a))

        elif operation['type'] == Operation.BITWISE_OR:
            a = stack.pop()
            b = stack.pop()
            stack.append(int(b | a))

        elif operation['type'] == Operation.PRINT:
            print(stack.pop())

        elif operation['type'] == Operation.GREATER:
            a = stack.pop()
            b = stack.pop()
            stack.append(int(b > a))

        elif operation['type'] == Operation.SMALLER:
            a = stack.pop()
            b = stack.pop()
            stack.append(int(b < a))

        elif operation['type'] == Operation.EQUAL:
            a = stack.pop()
            b = stack.pop()
            stack.append(int(a == b))

        elif operation['type'] == Keyword.IF:
            a = stack.pop()
            if a == 0:
                ip = operation['reference'] - 1

        elif operation['type'] == Keyword.ELSE:
            ip = operation['reference'] - 1

        elif operation['type'] == Keyword.END:
            ip = operation['reference'] - 1

        elif operation['type'] == Keyword.WHILE:
            pass

        elif operation['type'] == Keyword.DO:
            a = stack.pop()

            if a == 0:
                ip = operation['reference'] - 1

        elif operation['type'] == Operation.MEM:
            stack.append(STRING_CAPACITY)

        elif operation['type'] == Operation.LOAD8:
            address = stack.pop()
            byte = memory[address] % 0xFF
            stack.append(byte)

        elif operation['type'] == Operation.LOAD16:
            address = stack.pop()
            value = int.from_bytes(
                memory[address:address+2],
                byteorder="little")
            stack.append(value)

        elif operation['type'] == Operation.LOAD32:
            address = stack.pop()
            value = int.from_bytes(
                memory[address:address+4],
                byteorder="little")
            stack.append(value)

        elif operation['type'] == Operation.LOAD64:
            address = stack.pop()
            value = int.from_bytes(
                memory[address:address+8],
                byteorder="little")
            stack.append(value)

        elif operation['type'] == Operation.STORE8:
            address = stack.pop()
            value = stack.pop()
            memory[address] = value & 0xFF

        elif operation['type'] == Operation.STORE16:
            address = stack.pop()
            value = stack.pop()
            memory[address:address + 2] = value.to_bytes(
                length=2,
                byteorder="little",
                signed=(value < 0))

        elif operation['type'] == Operation.STORE32:
            address = stack.pop()
            value = stack.pop()
            memory[address:address + 4] = value.to_bytes(
                length=4,
                byteorder="little",
                signed=(value < 0))

        elif operation['type'] == Operation.STORE64:
            address = stack.pop()
            value = stack.pop()
            memory[address:address + 8] = value.to_bytes(
                length=8,
                byteorder="little",
                signed=(value < 0))
            print(memory[address])

        elif operation['type'] == Operation.SYSCALL0:
            syscall_num = stack.pop()
            emulate_unix(syscall_num, [])

        elif operation['type'] == Operation.SYSCALL1:
            syscall_num = stack.pop()
            emulate_unix(syscall_num, [stack.pop()])

        elif operation['type'] == Operation.SYSCALL2:
            syscall_num = stack.pop()
            emulate_unix(syscall_num, [stack.pop(), stack.pop()])

        elif operation['type'] == Operation.SYSCALL3:
            syscall_num = stack.pop()
            emulate_unix(syscall_num, [stack.pop(), stack.pop(), stack.pop()])

        elif operation['type'] == Operation.SYSCALL4:
            syscall_num = stack.pop()
            emulate_unix(syscall_num, [stack.pop(),
                                       stack.pop(), stack.pop(), stack.pop()])

        elif operation['type'] == Operation.SYSCALL5:
            syscall_num = stack.pop()
            emulate_unix(syscall_num, [stack.pop(), stack.pop(
            ), stack.pop(), stack.pop(), stack.pop()])

        elif operation['type'] == Operation.SYSCALL6:
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
