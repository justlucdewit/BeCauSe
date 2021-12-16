from modules.opcodes import Operation, Keyword, TokenType, scoped_instructions

from modules.stdlibs import stdlibs

BUILTIN_WORDS = {
    '>': Operation.GREATER,
    '<': Operation.SMALLER,
    '+': Operation.ADD,
    '*': Operation.MULTIPLY,
    '-': Operation.SUBTRACT,
    '>>': Operation.SHIFT_RIGHT,
    '<<': Operation.SHIFT_LEFT,
    '|': Operation.BITWISE_OR,
    '&': Operation.BITWISE_AND,
    'mod': Operation.MODULE,
    'dump': Operation.PRINT,
    '=': Operation.EQUAL,
    '!=': Operation.NOT_EQUAL,
    '>=': Operation.GREATER_EQUAL,
    '<=': Operation.SMALLER_EQUAL,
    'if': Keyword.IF,
    'else': Keyword.ELSE,
    'macro': Keyword.MACRO,
    'const': Keyword.CONST,
    'enum': Keyword.ENUM,
    'end': Keyword.END,
    'dup': Operation.DUP,
    '2dup': Operation.TWO_DUP,
    'drop': Operation.DROP,
    '2drop': Operation.TWO_DROP,
    'swap': Operation.SWAP,
    'over': Operation.OVER,
    'rot': Operation.ROT,
    'while': Keyword.WHILE,
    'do': Keyword.DO,
    'mem': Operation.MEM,
    '!8': Operation.STORE8,
    '!16': Operation.STORE16,
    '!32': Operation.STORE32,
    '!64': Operation.STORE64,
    '@8': Operation.LOAD8,
    '@16': Operation.LOAD16,
    '@32': Operation.LOAD32,
    '@64': Operation.LOAD64,
    'syscall0': Operation.SYSCALL0,
    'syscall1': Operation.SYSCALL1,
    'syscall2': Operation.SYSCALL2,
    'syscall3': Operation.SYSCALL3,
    'syscall4': Operation.SYSCALL4,
    'syscall5': Operation.SYSCALL5,
    'syscall6': Operation.SYSCALL6,
    'import': Keyword.IMPORT,
    'memory': Keyword.MEMORY,
    'here': Operation.HERE
}

scoped_builtin_words = list(filter(
    lambda x: BUILTIN_WORDS[x] in scoped_instructions, BUILTIN_WORDS.keys()))


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
        return (TokenType.INT, int(token_as_text))
    except ValueError:
        return (TokenType.WORD, token_as_text)


def lex_line(file_path, row, line):
    col = find_col(line, 0, lambda x: not x.isspace())
    while col < len(line):
        col_end = None

        if line[col] == '"':
            col_end = find_col(line, col + 1, lambda x: x == '"')
            if col_end >= len(line) or line[col_end] != '\"':
                print(
                    f"{file_path}:{row + 1}:{col + 1}:"
                    "\n\tUnclosed character literal")
                exit(1)

            text_of_token = bytes(
                line[col + 1:col_end], 'utf-8').decode("unicode_escape")

            yield (col, (TokenType.STRING, text_of_token))
            col = find_col(line, col_end + 1, lambda x: not x.isspace())
        elif line[col] == '\'':
            col_end = find_col(line, col + 1, lambda x: x == '\'')
            if col_end >= len(line) or line[col_end] != '\'':
                print(
                    f"{file_path}:{row + 1}:{col + 1}:\n\tUnclosed character "
                    "literal")
                exit(1)

            text_of_token = bytes(
                line[col + 1:col_end], 'utf-8').decode("unicode_escape")

            if len(text_of_token) > 1:
                print(
                    f"{file_path}:{row + 1}:{col + 1}:\n\tCharacter literal "
                    "found with multiple characters, use string instead")
                exit(1)

            if len(text_of_token) == 0:
                print(
                    f"{file_path}:{row + 1}:{col + 1}:\n\tCharacter literal "
                    "found no character inside, use string instead")
                exit(1)

            yield (col, (TokenType.CHAR, text_of_token))
            col = find_col(line, col_end + 1, lambda x: not x.isspace())
        else:
            col_end = find_col(line, col, lambda x: x.isspace())
            yield (col, lex_word(line[col:col_end]))
            col = find_col(line, col_end, lambda x: not x.isspace())


macros = {}
memory_regions = {}
imports = []


def crossreference_blocks(tokens, file_path):
    reversed_program = list(reversed(tokens))
    stack = []
    ip = 0
    program = []

    while len(reversed_program) > 0:
        token = reversed_program.pop()

        op = None
        if token['type'] == TokenType.INT:
            op = {'type': Operation.PUSH_INT, 'value': int(
                token['value']), 'loc': token['loc']}
        elif token['type'] == TokenType.STRING:
            op = {'type': Operation.PUSH_STRING,
                  'value': token['value'], 'loc': token['loc']}
        elif token['type'] == TokenType.CHAR:
            op = {'type': Operation.PUSH_INT,
                  'value': ord(token['value']), 'loc': token['loc']}
        elif token['type'] == TokenType.WORD:
            if token['value'] in BUILTIN_WORDS:
                op = {
                    'type': BUILTIN_WORDS[token['value']],
                    'loc': token['loc']
                }
            elif token['value'] in macros:
                reversed_program += reversed(macros[token['value']]['tokens'])
                continue
            else:
                (file_path, row, col) = token['loc']
                word = token['value']
                print(f"{file_path}:{row}:{col}:\n\tUnexpected word '{word}'")
                exit(1)

        if op['type'] == Keyword.IF:
            program.append(op)
            stack.append(ip)
            ip += 1

        elif op['type'] == Keyword.ELSE:
            program.append(op)
            if_ip = stack.pop()

            if program[if_ip]['type'] != Keyword.IF:
                print("Parse Error: else can only be used with 'if' blocks")
                exit(1)

            program[if_ip]['reference'] = ip + 1
            stack.append(ip)
            ip += 1

        elif op['type'] == Keyword.END:
            program.append(op)
            block_ip = stack.pop()

            if (program[block_ip]['type'] == Keyword.IF or
                    program[block_ip]['type'] == Keyword.ELSE):
                program[block_ip]['reference'] = ip
                program[ip]['reference'] = ip + 1

            elif program[block_ip]['type'] == Keyword.DO:
                program[ip]['reference'] = program[block_ip]['reference']
                program[block_ip]['reference'] = ip + 1

            else:
                print(
                    "Parse Error: end can only be use to close 'if', 'else', "
                    "'do' and 'macro' blocks")
                exit(1)
            ip += 1

        elif op['type'] == Keyword.WHILE:
            program.append(op)
            stack.append(ip)
            ip += 1

        elif op['type'] == Keyword.DO:
            program.append(op)
            while_ip = stack.pop()
            program[ip]['reference'] = while_ip
            stack.append(ip)
            ip += 1

        elif op['type'] == Keyword.IMPORT:
            # Import must be followed by a string containing the file
            if (len(reversed_program) == 0 or
                    reversed_program[len(reversed_program) - 1]
                    ['type'] != TokenType.STRING):

                (file_path, row, col) = op['loc']
                print(
                    f"{file_path}:{row}:{col}:\n\tWrong usage of import"
                    "feature\n\timport must be followed by a string containing"
                    " the path to the file to import\n\tfor example:\n\n\t"
                    "import \"std/io\"")
                exit(1)

            import_path_token = reversed_program.pop()
            result = None
            imports.append(import_path_token['value'])

            if import_path_token['value'] in stdlibs:
                result = lex_text(
                    import_path_token['value'],
                    stdlibs[import_path_token['value']])
            else:
                local_base_path = "/".join(file_path.split('/')[:-1])
                if local_base_path != "":
                    local_base_path = local_base_path + "/"

                try:
                    result = lex_file(local_base_path +
                                      import_path_token['value'] + ".bcs")
                except FileNotFoundError:
                    (file_path, row, col) = op['loc']

                    full_file_name = local_base_path + \
                        import_path_token['value'] + '.bcs'

                    print(
                        f"{file_path}:{row}:{col}:\n\tCould not find file "
                        f"{full_file_name} to import")

                    exit(1)

            reversed_program += reversed(result)

        elif op['type'] == Keyword.MEMORY:
            # Import must be followed by a string containing the file
            if (len(reversed_program) == 0 or
                    reversed_program[len(reversed_program) - 1]
                    ['type'] != TokenType.WORD):

                (file_path, row, col) = op['loc']
                print(
                    f"{file_path}:{row}:{col}:\n\tWrong usage of memory "
                    "region feature\n\tmemory keyword must be followed by a "
                    "word that will be used as the reference to the memory "
                    "region. \n\tfor example:\n\n\t"
                    "memory pointer_to_mem\n\t\t64000\n\tend")
                exit(1)

            # Get the name of the memory region
            name_of_memory_region = reversed_program.pop()

            end_found = False
            evaluation_stack = []
            while len(reversed_program) > 0:
                t = reversed_program.pop()
                print(t)

                # TODO: allow macros here
                if (t['type'] == TokenType.WORD and
                        BUILTIN_WORDS.get(t['value']) == Keyword.END):
                    end_found = True
                    break
                elif t['type'] == TokenType.INT:
                    evaluation_stack.append(t['value'])
                elif (t['type'] == TokenType.WORD and
                        BUILTIN_WORDS.get(t['value']) == Operation.ADD):
                    a = evaluation_stack.pop()
                    b = evaluation_stack.pop()
                    evaluation_stack.append(a + b)
                elif (t['type'] == TokenType.WORD and
                        BUILTIN_WORDS.get(t['value']) == Operation.MULTIPLY):
                    a = evaluation_stack.pop()
                    b = evaluation_stack.pop()
                    evaluation_stack.append(a * b)

            print('---------', evaluation_stack)

            if not end_found:
                (file_path, row, col) = op['loc']
                print(
                    f"{file_path}:{row}:{col}:\n\tFound memory region that was"
                    " not closed with 'end' keyword")
                exit(1)

            # TODO get the size from the evualtion stack
            memory_regions[name_of_memory_region['value']] = 0
        elif op['type'] == Keyword.CONST:
            # Const must be followed by a word, describing the name of the
            # constant
            if len(reversed_program) == 0:
                (file_path, row, col) = op['loc']

                print(
                    f"{file_path}:{row}:{col}:\n\tWrong usage of const "
                    " feature\n\tconst keyword must be followed by a "
                    "word that will be used as the reference to the value."
                    "\n\tfor example:\n\n\t"
                    "const meaning_of_life 64000\n")
                exit(1)

            # Get the name of the constant
            constant_name_token = reversed_program.pop()

            if constant_name_token['type'] != TokenType.WORD:
                (file_path, row, col) = constant_name_token['loc']
                constant_name = constant_name_token['value']
                tokentype_str = "unknown"

                if constant_name_token['type'] == TokenType.STRING:
                    tokentype_str = "string"
                elif constant_name_token['type'] == TokenType.INT:
                    tokentype_str = "integer"
                elif constant_name_token['type'] == TokenType.CHAR:
                    tokentype_str = "character"

                print(
                    f"{file_path}:{row}:{col}:\n\tInvalid constant name. "
                    f"expected a word, got {tokentype_str} '{constant_name}'")
                exit(1)

            constant_name = constant_name_token['value']

            # Make sure no 2 constants with same name get defined
            if constant_name in macros:
                (file_path, row, col) = constant_name_token['loc']
                (macro_file_path, macro_row,
                 macro_col) = macros[constant_name]['loc']
                print(
                    f"{file_path}:{row}:{col}:\n\tConstant '{constant_name}' "
                    f"already exists at {macro_file_path}:{macro_row}:"
                    f"{macro_col}")
                exit(1)

            # Make sure no builtins get overridden by macros
            if constant_name in BUILTIN_WORDS:
                (file_path, row, col) = constant_name_token['loc']

                print(
                    f"{file_path}:{row}:{col}:\n\tConstant '{constant_name}' "
                    "is overriding a built-in word")

                exit(1)

            if len(reversed_program) <= 0:
                (file_path, row, col) = op['loc']

                print(
                    f"{file_path}:{row}:{col}:\n\tWrong usage of const "
                    " feature"
                    "\n\tName of constant must be followed by a number or a"
                    "\n\tstring. For example:\n\n\t"
                    "const meaning_of_life 64000\n")
                exit(1)

            constant = {
                'loc': constant_name_token['loc'],
                'tokens': [reversed_program.pop()]
            }

            macros[constant_name] = constant

        elif op['type'] == Keyword.MACRO:

            # Macro must be followed by a name, code and 'end'
            if len(reversed_program) == 0:
                (file_path, row, col) = op['loc']

                print(
                    f"{file_path}:{row}:{col}:\n\tWrong usage of macro "
                    "feature\n\tmacro must be followed by a name, then some "
                    "code, then the 'end keyword'.\n\tfor Example:\n\n\tmacro "
                    "write\n\t\t1 1 syscall3\n\tend")

                exit(1)

            # Get the token name
            macro_name_token = reversed_program.pop()

            if macro_name_token['type'] != TokenType.WORD:
                (file_path, row, col) = macro_name_token['loc']
                macro_name = macro_name_token['value']
                tokentype_str = "unknown"

                if macro_name_token['type'] == TokenType.STRING:
                    tokentype_str = "string"
                elif macro_name_token['type'] == TokenType.INT:
                    tokentype_str = "integer"
                elif macro_name_token['type'] == TokenType.CHAR:
                    tokentype_str = "character"

                print(
                    f"{file_path}:{row}:{col}:\n\tInvalid macro name. expected"
                    f" a word, got {tokentype_str} '{macro_name}'")
                exit(1)

            macro_name = macro_name_token['value']

            # Make sure no 2 macros with same name get defined
            if macro_name in macros:
                (file_path, row, col) = macro_name_token['loc']
                (macro_file_path, macro_row,
                 macro_col) = macros[macro_name]['loc']
                macro_name = macro_name_token['value']
                print(
                    f"{file_path}:{row}:{col}:\n\tMacro '{macro_name}' already"
                    f" exists at {macro_file_path}:{macro_row}:{macro_col}")
                exit(1)

            # Make sure no builtins get overridden by macros
            if macro_name in BUILTIN_WORDS:
                (file_path, row, col) = macro_name_token['loc']
                macro_name = macro_name_token['value']

                print(
                    f"{file_path}:{row}:{col}:\n\tMacro '{macro_name}' is "
                    "overriding a built-in word")

                exit(1)

            macro = {
                'loc': op['loc'],
                'tokens': []
            }

            nestingDepth = 0

            while len(reversed_program) > 0:
                token = reversed_program.pop()

                if (token['type'] == TokenType.WORD and
                        token['value'] in scoped_builtin_words):
                    macro['tokens'].append(token)
                    nestingDepth += 1
                elif (token['type'] == TokenType.WORD and
                        token['value'] == 'end'):
                    if nestingDepth == 0:
                        break
                    else:
                        macro['tokens'].append(token)
                        nestingDepth -= 1
                else:
                    macro['tokens'].append(token)

            if token['type'] != TokenType.WORD or token['value'] != 'end':
                (file_path, row, col) = token['loc']
                print(
                    f"{file_path}:{row}:{col}:\n\tMacros must end with 'end' "
                    "keyword")
                exit(1)

            macros[macro_name] = macro
        elif op['type'] == Keyword.ENUM:
            current_op = reversed_program.pop()
            enum_name_token = current_op

            if enum_name_token['type'] != TokenType.WORD:
                (file_path, row, col) = enum_name_token['loc']
                print(
                    f"{file_path}:{row}:{col}:\n\tWrong usage of enum feature"
                    "\n\tenum name must be a word, For example: \n\n\t"
                    "enum DAYS"
                    "\n\t\tMONDAY"
                    "\n\t\tTUESDAY"
                    "\n\t\tWEDNESDAY"
                    "\n\t\tTHURSDAY"
                    "\n\t\tFRIDAY"
                    "\n\t\tSATURDAY"
                    "\n\t\tSUNDAY"
                    "\n\tend")
                exit(1)

            i = 0
            enum_name = enum_name_token['value']
            current_op = reversed_program.pop()
            while current_op['value'] != 'end':
                enum_member_name = current_op['value']

                enum_member = {
                    'loc': enum_name_token['loc'],
                    'tokens': [
                        {
                            'loc': enum_name_token['loc'],
                            'type': TokenType.INT,
                            'value': i
                        }
                    ]
                }

                i += 1
                macros[f"{enum_name}:{enum_member_name}"] = enum_member
                current_op = reversed_program.pop()

                if current_op['type'] != TokenType.WORD:
                    (file_path, row, col) = current_op['loc']
                    print(
                        f"{file_path}:{row}:{col}:\n\t Values in enumerations "
                        "can only be words, not numbers, strings, characters "
                        "or other token types")
                    exit(1)

                if len(reversed_program) == 0 and current_op['value'] != 'end':
                    (file_path, row, col) = enum_name_token['loc']
                    print(
                        f"{file_path}:{row}:{col}:\n\tUnterminated enumeration"
                    )
                    exit(1)
        elif op['type'] == Operation.HERE:
            (file_path, row, col) = op['loc']

            program.append({
                'type': Operation.PUSH_STRING,
                'value': f"{file_path}:{row}:{col}",
                'loc': op['loc']
            })
        else:
            program.append(op)
            ip += 1

    return program


def preprocess_file(file_content):
    return list(map(lambda x: x.split('//')[0], file_content))


def lex_file(file_path):
    with open(file_path, "r") as f:
        # Plus 1 because we want it to be 1 indexed
        return [{'loc': (file_path, row + 1, col + 1),
                 'type': token_type,
                 'value': token_value}
                for (row, line) in enumerate(preprocess_file(f.readlines()))
                for (col, (token_type, token_value)) in lex_line(
                    file_path,
                    row,
                    line)
                ]


def lex_text(file_path, text):
    text = text.splitlines()
    # Plus 1 because we want it to be 1 indexed
    return [{'loc': (file_path, row + 1, col + 1),
             'type': token_type,
             'value': token_value}
            for (row, line) in enumerate(preprocess_file(text))
            for (col, (token_type, token_value)) in lex_line(
                file_path,
                row,
                line)
            ]


def load_program_from_file(file_path):
    # Parse token as op
    return crossreference_blocks(lex_file(file_path), file_path)
