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
            if_addr = stack.pop()
            program[if_addr] = (OP_IF, ip + 1)
            stack.append(ip)

        elif op[0] == OP_END:
            block_start_addr = stack.pop()
            if program[block_start_addr][0] == OP_IF or program[block_start_addr][0] == OP_ELSE:
                program[block_start_addr] = (program[block_start_addr][0], ip)
                program[block_start_addr] = (OP_END, ip + 1)
            elif program[block_start_addr][0] == OP_DO:
                program[ip] = (OP_END, program[block_start_addr][1])
                program[block_start_addr] = (OP_DO, ip + 1)

            else:
                print("ERROR: else can only be used to close 'if' and 'else' and 'do' blocks")
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