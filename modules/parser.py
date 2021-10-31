from modules.opcodes import *

def parse_token_as_op(token):
    (file_path, row, col, word) = token
    if word == '>':
        return (OP_GREATER, )
    elif word == '<':
        return (OP_SMALLER, )
    elif word == '+':
        return (OP_ADD, )
    elif word == '-':
        return (OP_SUBTRACT, )
    elif word == '>>':
        return (OP_SHIFT_RIGHT, )
    elif word == '<<':
        return (OP_SHIFT_LEFT, )
    elif word == '|':
        return (OP_BITWISE_OR, )
    elif word == '&':
        return (OP_BITWISE_AND, )
    elif word == 'dump':
        return (OP_PRINT, )
    elif word == '=':
        return (OP_EQUAL, )
    elif word == 'if':
        return (OP_IF, )
    elif word == 'else':
        return (OP_ELSE, )
    elif word == 'end':
        return (OP_END, )
    elif word == 'dup':
        return (OP_DUP, )
    elif word == '2dup':
        return (OP_2DUP, )
    elif word == 'drop':
        return (OP_DROP, )
    elif word == 'while':
        return (OP_WHILE, )
    elif word == 'do':
        return (OP_DO, )
    elif word == 'mem':
        return (OP_MEM, )
    elif word == '.':
        return (OP_STORE, )
    elif word == ',':
        return (OP_LOAD, )
    elif word == 'syscall0':
        return (OP_SYSCALL0, )
    elif word == 'syscall1':
        return (OP_SYSCALL1, )
    elif word == 'syscall2':
        return (OP_SYSCALL2, )
    elif word == 'syscall3':
        return (OP_SYSCALL3, )
    elif word == 'syscall4':
        return (OP_SYSCALL4, )
    elif word == 'syscall5':
        return (OP_SYSCALL5, )
    elif word == 'syscall6':
        return (OP_SYSCALL6, )
    else:
        try:
            return (OP_PUSH, int(word))
        except ValueError:
            print(f"{file_path}:{row + 1}:{col + 1}:\n\tUnexpected token '{word}'")
            exit(-1)

def find_col(line, start, predicate):
    while start < len(line) and not predicate(line[start]):
        start += 1
    return start

def strip_col(line, col):
    while col < len(line) and line[col].isspace():
        col += 1
    return col

def chop_word(line, col):
    while col < len(line) and not line[col].isspace():
        col += 1
    return col

def lex_line(line):
    col = find_col(line, 0, lambda x: not x.isspace())
    while col < len(line):
        col_end = find_col(line, col, lambda x: x.isspace())
        yield (col, line[col:col_end])
        col = find_col(line, col_end, lambda x: not x.isspace())

def crossreference_blocks(program):
    stack = []
    for ip in range(len(program)):
        op = program[ip]
        if op[0] == OP_IF:
            stack.append(ip)

        elif op[0] == OP_ELSE:
            if_ip = stack.pop()

            if program[if_ip][0] != OP_IF:
                print("Parse Error: else can only be used with 'if' blocks")
                exit(-1)

            program[if_ip] = (OP_IF, ip + 1)
            stack.append(ip)

        elif op[0] == OP_END:
            block_ip = stack.pop()
            if program[block_ip][0] == OP_IF or program[block_ip][0] == OP_ELSE:
                program[block_ip] = (program[block_ip][0], ip)
                program[ip] = (OP_END, ip + 1)
            elif program[block_ip][0] == OP_DO:
                program[ip] = (OP_END, program[block_ip][1])
                program[block_ip] = (OP_DO, ip + 1)

            else:
                print("Parse Error: end can only be used to close 'if' and 'else' and 'do' blocks")
                exit(-1)

        elif op[0] == OP_WHILE:
            stack.append(ip)

        elif op[0] == OP_DO:
            while_ip = stack.pop()
            program[ip] = (OP_DO, while_ip)
            stack.append(ip)
            
    return program

def preprocess_file(file_content):
    return list(map(lambda x: x.split('//')[0], file_content))

def lex_file(file_path):
    with open(file_path, "r") as f:
        return [(file_path, row, col, token)
            for (row, line) in enumerate(preprocess_file(f.readlines()))
            for (col, token) in lex_line(line)]

def load_program_from_file(file_path):
    return crossreference_blocks([parse_token_as_op(token) for token in lex_file(file_path)])