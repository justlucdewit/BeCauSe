from modules.opcodes import *

BUILDIN_WORDS = {
    '>': OP_GREATER,
    '<': OP_SMALLER,
    '+': OP_ADD,
    '-': OP_SUBTRACT,
    '>>': OP_SHIFT_RIGHT,
    '<<': OP_SHIFT_LEFT,
    '|': OP_BITWISE_OR,
    '&': OP_BITWISE_AND,
    'dump': OP_PRINT,
    '=': OP_EQUAL,
    'if': OP_IF,
    'else': OP_ELSE,
    'end': OP_END,
    'dup': OP_DUP,
    '2dup': OP_2DUP,
    'drop': OP_DROP,
    'swap': OP_SWAP,
    'over': OP_OVER,
    'while': OP_WHILE,
    'do': OP_DO,
    'mem': OP_MEM,
    '.': OP_STORE,
    ',': OP_LOAD,
    'syscall0': OP_SYSCALL0,
    'syscall1': OP_SYSCALL1,
    'syscall2': OP_SYSCALL2,
    'syscall3': OP_SYSCALL3,
    'syscall4': OP_SYSCALL4,
    'syscall5': OP_SYSCALL5,
    'syscall6': OP_SYSCALL6,
}


def parse_token_as_op(token):
    if token['type'] == TOK_INT:
        return {'type': OP_PUSH, 'value': int(token['value']), 'loc': token['loc']}
    elif token['type'] == TOK_WORD:
        if token['value'] in BUILDIN_WORDS:
            return {'type': BUILDIN_WORDS[token['value']], 'loc': token['loc']}
        else:
            (file_path, row, col) = token['loc']
            word = token['value']
            print(
                f"{file_path}:{row}:{col}:\n\tUnexpected word '{word}'")
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


def lex_word(token_as_text):
    try:
        return (TOK_INT, int(token_as_text))
    except ValueError:
        return (TOK_WORD, token_as_text)


def lex_line(line):
    col = find_col(line, 0, lambda x: not x.isspace())
    while col < len(line):
        col_end = find_col(line, col, lambda x: x.isspace())
        yield (col, lex_word(line[col:col_end]))
        col = find_col(line, col_end, lambda x: not x.isspace())


def crossreference_blocks(program):
    stack = []
    for ip in range(len(program)):
        op = program[ip]
        if op['type'] == OP_IF:
            stack.append(ip)

        elif op['type'] == OP_ELSE:
            if_ip = stack.pop()

            if program[if_ip]['type'] != OP_IF:
                print("Parse Error: else can only be used with 'if' blocks")
                exit(-1)

            program[if_ip]['reference'] = ip + 1
            stack.append(ip)

        elif op['type'] == OP_END:
            block_ip = stack.pop()

            if program[block_ip]['type'] == OP_IF or program[block_ip]['type'] == OP_ELSE:
                program[block_ip]['reference'] = ip
                program[ip]['reference'] = ip + 1

            elif program[block_ip]['type'] == OP_DO:
                program[ip]['reference'] = program[block_ip]['reference']
                program[block_ip]['reference'] = ip + 1

            else:
                print(
                    "Parse Error: end can only be used to close 'if' and 'else' and 'do' blocks")
                exit(-1)

        elif op['type'] == OP_WHILE:
            stack.append(ip)

        elif op['type'] == OP_DO:
            while_ip = stack.pop()
            program[ip]['reference'] = while_ip
            stack.append(ip)

    return program


def preprocess_file(file_content):
    return list(map(lambda x: x.split('//')[0], file_content))


def lex_file(file_path):
    with open(file_path, "r") as f:
        return [{'loc': (file_path, row + 1, col + 1),  # Plus 1 because we want it to be 1 indexed
                 'type': token_type,
                 'value': token_value}
                for (row, line) in enumerate(preprocess_file(f.readlines()))
                for (col, (token_type, token_value)) in lex_line(line)]


def load_program_from_file(file_path):
    return crossreference_blocks([parse_token_as_op(token) for token in lex_file(file_path)])
