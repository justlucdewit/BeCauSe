from modules.opcodes import *
from modules.stdlibs import *

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
    'macro': OP_MACRO,
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
    'import': OP_IMPORT
}


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
        col_end = None

        if line[col] == '"':
            col_end = find_col(line, col + 1, lambda x: x == '"')
            text_of_token = bytes(
                line[col + 1:col_end], 'utf-8').decode("unicode_escape")

            yield (col, (TOK_STRING, text_of_token))
            col = find_col(line, col_end + 1, lambda x: not x.isspace())
        else:
            col_end = find_col(line, col, lambda x: x.isspace())
            yield (col, lex_word(line[col:col_end]))
            col = find_col(line, col_end, lambda x: not x.isspace())


def crossreference_blocks(tokens, file_path):
    reversed_program = list(reversed(tokens))
    stack = []
    ip = 0
    macros = {}
    program = []

    while len(reversed_program) > 0:
        token = reversed_program.pop()
        op = None
        if token['type'] == TOK_INT:
            op = {'type': OP_PUSH, 'value': int(
                token['value']), 'loc': token['loc']}
        elif token['type'] == TOK_STRING:
            op = {'type': OP_PUSH_STRING,
                  'value': token['value'], 'loc': token['loc']}
        elif token['type'] == TOK_WORD:
            if token['value'] in BUILDIN_WORDS:
                op = {
                    'type': BUILDIN_WORDS[token['value']], 'loc': token['loc']}
            elif token['value'] in macros:
                reversed_program += reversed(macros[token['value']]['tokens'])
                continue
            else:
                (file_path, row, col) = token['loc']
                word = token['value']
                print(f"{file_path}:{row}:{col}:\n\tUnexpected word '{word}'")
                exit(1)

        if op['type'] == OP_IF:
            program.append(op)
            stack.append(ip)
            ip += 1

        elif op['type'] == OP_ELSE:
            program.append(op)
            if_ip = stack.pop()

            if program[if_ip]['type'] != OP_IF:
                print("Parse Error: else can only be used with 'if' blocks")
                exit(1)

            program[if_ip]['reference'] = ip + 1
            stack.append(ip)
            ip += 1

        elif op['type'] == OP_END:
            program.append(op)
            block_ip = stack.pop()

            if program[block_ip]['type'] == OP_IF or program[block_ip]['type'] == OP_ELSE:
                program[block_ip]['reference'] = ip
                program[ip]['reference'] = ip + 1

            elif program[block_ip]['type'] == OP_DO:
                program[ip]['reference'] = program[block_ip]['reference']
                program[block_ip]['reference'] = ip + 1

            else:
                print(
                    "Parse Error: end can only be used to close 'if', 'else', 'do' and 'macro' blocks")
                exit(1)
            ip += 1

        elif op['type'] == OP_WHILE:
            program.append(op)
            stack.append(ip)
            ip += 1

        elif op['type'] == OP_DO:
            program.append(op)
            while_ip = stack.pop()
            program[ip]['reference'] = while_ip
            stack.append(ip)
            ip += 1

        elif op['type'] == OP_IMPORT:
            # Import must be followed by a string containing the file
            if len(reversed_program) == 0 or reversed_program[len(reversed_program) - 1]['type'] != TOK_STRING:
                (file_path, row, col) = op['loc']
                print(f"{file_path}:{row}:{col}:\n\tWrong usage of import feature\n\timport must be followed by a string containing the path to the file to import\n\tfor Example:\n\n\timport \"std/io\"")
                exit(1)

            import_path_token = reversed_program.pop()
            result = None

            if import_path_token['value'] in stdlibs:
                result = lex_text(
                    import_path_token['value'], stdlibs[import_path_token['value']])
            else:
                local_base_path = "/".join(file_path.split('/')[:-1])
                if local_base_path != "":
                    local_base_path = local_base_path + "/"

                try:
                    result = lex_file(local_base_path +
                                      import_path_token['value'] + ".bcs")
                except FileNotFoundError:
                    (file_path, row, col) = op['loc']
                    print(
                        f"{file_path}:{row}:{col}:\n\tCould not find file {local_base_path + import_path_token['value'] + '.bcs'} to import")
                    exit(1)

            reversed_program += reversed(result)

        elif op['type'] == OP_MACRO:
            # Macro must be followed by a name, code and 'end'
            if len(reversed_program) == 0:
                (file_path, row, col) = op['loc']
                print(f"{file_path}:{row}:{col}:\n\tWrong usage of macro feature\n\tmacro must be followed by a name, then some code, then the 'end keyword'.\n\tfor Example:\n\n\tmacro write\n\t\t1 1 syscall3\n\tend")
                exit(1)

            # Get the token name
            macro_name_token = reversed_program.pop()

            if macro_name_token['type'] != TOK_WORD:
                (file_path, row, col) = macro_name_token['loc']
                macro_name = macro_name_token['value']
                tokentype_str = "unknown"

                if macro_name_token['type'] == TOK_STRING:
                    tokentype_str = "string"
                elif macro_name_token['type'] == TOK_INT:
                    tokentype_str = "integer"

                print(
                    f"{file_path}:{row}:{col}:\n\tInvalid macro name. expected a word, got {tokentype_str} '{macro_name}'")
                exit(1)

            macro_name = macro_name_token['value']

            # Make sure no 2 macros with same name get defined
            if macro_name in macros:
                (file_path, row, col) = macro_name_token['loc']
                (macro_file_path, macro_row,
                 macro_col) = macros[macro_name]['loc']
                print(
                    f"{file_path}:{row}:{col}:\n\tMacro '{macro_name_token['value']}' already exists at {macro_file_path}:{macro_row}:{macro_col}")
                exit(1)

            # Make sure no buildins get overridden by macros
            if macro_name in BUILDIN_WORDS:
                (file_path, row, col) = macro_name_token['loc']
                print(
                    f"{file_path}:{row}:{col}:\n\tMacro '{macro_name_token['value']}' is overriding a build-in word")
                exit(1)

            macro = {
                'loc': op['loc'],
                'tokens': []
            }

            while len(reversed_program) > 0:
                token = reversed_program.pop()

                if token['type'] == TOK_WORD and token['value'] == 'end':
                    break
                else:
                    macro['tokens'].append(token)

            if token['type'] != TOK_WORD or token['value'] != 'end':
                (file_path, row, col) = token['loc']
                print(
                    f"{file_path}:{row}:{col}:\n\tMacros must end with 'end' keyword")
                exit(1)

            macros[macro_name] = macro
        else:
            program.append(op)
            ip += 1

    # for token in program:
    #     name = instructions_map[token['type']]
    #     if 'value' in token:
    #         name += f" {token['value']}"
    #     print(name)

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


def lex_text(file_path, text):
    text = text.splitlines()
    return [{'loc': (file_path, row + 1, col + 1),  # Plus 1 because we want it to be 1 indexed
             'type': token_type,
             'value': token_value}
            for (row, line) in enumerate(preprocess_file(text))
            for (col, (token_type, token_value)) in lex_line(line)]


def load_program_from_file(file_path):
    # Parse token as op
    return crossreference_blocks(lex_file(file_path), file_path)
