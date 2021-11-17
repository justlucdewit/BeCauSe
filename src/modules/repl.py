from modules.run_program import run_program, stack
from modules.parser import lex_text, crossreference_blocks, imports


def repl():
    print("BeCauSe REPL")

    while True:
        code = input(">>> ")

        if code.startswith(":"):
            tokens = code.split(" ")
            command = tokens[0]

            if command == ":q":
                exit(0)

            elif command == ":h":
                print(
                    "\n"
                    "Command\t\tDescription\n"
                    "----------------------------------------\n"
                    ":h\t\tPrint this help overview\n"
                    ":q\t\tExit the REPL\n"
                    ":i\t\tList the currently imported libraries\n"
                    ":s <N>\t\tShow the top N values on the stack\n"
                )

            elif command == ":i":
                if len(imports) == 0:
                    print("no libs imported\n")

                else:
                    for lib in imports:
                        print(f"- {lib}")
                    print()

            elif command == ":s":
                n = None

                try:
                    n = int(tokens[1])
                except BaseException:
                    print(":s needs numeric value as first argument\n")

                if n is not None:
                    stack_segment = list(reversed(stack))[:n]
                    for i, n in enumerate(stack_segment):
                        print(f"top - {i} \t\t {n}")
                    print()

            else:
                print("unknown command, try :h\n")
        else:
            try:
                lex_result = lex_text("repl input", code)
                program = crossreference_blocks(lex_result, "repl input")
                run_program(program)
            finally:
                pass

            print()
