#!/usr/bin/env python3

# Import custom modules
from modules.compile_program import compile_program_linux_x86_64
from modules.parser import load_program_from_file
from modules.repl import repl
from modules.run_program import run_program
from modules.argument_parser import args
from datetime import datetime

start_timestamp = datetime.now().timestamp()

# Version string
BCS_VERSION = "BCS Compiler/Interpreter V1.0.0"

# Determine if there were any arguments given to the program
no_args_given = (not args.debug and
                 not args.interpret and
                 not args.run and
                 not args.version and
                 args.output is None and
                 args.filename == '')

# Entry point to the program
if __name__ == "__main__":

    # If no arguments were given to the program
    if no_args_given:
        repl()

    # If --version argument was given, print version
    elif args.version:
        print(BCS_VERSION)
        print("""
                            # #
                          # # # #
                        # # # # # #
                        # # # # # # #
                          # # # # # # #
                            # # # # # # #
# # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # #
                                      # # # # # #
                                        # # # # # #
                                          # # # # # #
                                          # # # # # # #
                # # # # # # # # # # # # # # # # # # #
                  # # # # # # # # # # # # # # # # #
                    # # # # # # # # # # # # # # #
                                    # # # # # #
                                  # # # # # #
                                # # # # # #
                              # # # # # #
                              # # # # #
                                # # #
                                  #
        """)
        exit(0)

    # If interpretation mode, interpret the program
    elif args.interpret:
        program = load_program_from_file(args.filename)
        run_program(program)

        if args.time:
            interpretation_end = datetime.now().timestamp()
            interpretation_took = interpretation_end - start_timestamp
            print(
                '\ninterpretation finished, took'
                f' {interpretation_took:.3f}sec\n')

    # If compilation mode, compile the program
    else:
        if args.filename == '':
            print("error: no input file given\n")
            exit(-1)

        program = load_program_from_file(args.filename)
        compile_program_linux_x86_64(program, args.output, args.debug)

        if args.time:
            compilation_end = datetime.now().timestamp()
            compilation_took = compilation_end - start_timestamp
            print(
                'compilation finished, took'
                f' {compilation_took:.3f}sec\n')
