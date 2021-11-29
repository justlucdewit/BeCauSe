#!/usr/bin/env python3

# Import custom modules
from io import TextIOWrapper
import multiprocessing

import sys
from modules.compile_program import compile_assembly, compile_program_linux_x86_64
from modules.parser import load_program_from_file
from modules.repl import repl
from modules.run_program import run_program
from modules.argument_parser import args
from datetime import datetime
import signal

from os import error, remove, stat
from time import sleep

start_timestamp = datetime.now().timestamp()


def signal_handler(sig, frame):
    try:
        outfile.close()
        remove(str(pid) + ".out")
    except Exception as e:
        print(e)
    sys.exit(0)

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
    signal.signal(signal.SIGINT, signal_handler)
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
        # program = load_program_from_file(args.filename)
        if args.watch:
            has_errored = True
            exit_program = False
            last_changes = stat(args.filename).st_mtime
            
            outfile = TextIOWrapper
            while(exit_program is False):
                while(has_errored is True):
                    try:
                        program = load_program_from_file(args.filename)
                        process = multiprocessing.Process(target=run_program,
                                                          args=[program])
                        last_changes = stat(args.filename).st_mtime
                        process.start()

                        print(process.pid)
                        pid = process.pid
                        outfile = open(str(process.pid) + ".out", "w")
                        # sys.stdout = outfile
                    except Exception as e:
                        print(e)
                        print(last_changes)
                        has_errored = True
                        while(last_changes == stat(args.filename).st_mtime):
                            sleep(0.1)
                    has_errored = False

                while(1):
                    current_changes = stat(args.filename).st_mtime
                    if(last_changes != current_changes):
                        process.terminate()
                        outfile.close()
                        remove(str(pid) + ".out")
                        has_errored = True
                        break

        else:
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

        if args.watch:
            has_errored = True
            exit_program = False
            last_changes = stat(args.filename).st_mtime
            outfile = TextIOWrapper

            while(exit_program is False):
                while(has_errored is True):
                    try:
                        program = load_program_from_file(args.filename)
                        compile_program_linux_x86_64(program, args.output, args.debug)
                        process = multiprocessing.Process(target=compile_assembly,
                                                          args=[args.output, args.debug])
                        last_changes = stat(args.filename).st_mtime
                        process.start()

                        print(process.pid)
                        pid = process.pid
                        outfile = open(str(process.pid) + ".out", "w")
                        # sys.stdout = outfile
                    except Exception as e:
                        print(e)
                        print(last_changes)
                        has_errored = True

                        while(last_changes == stat(args.filename).st_mtime):
                            sleep(0.1)
                    has_errored = False

                while(1):
                    current_changes = stat(args.filename).st_mtime
                    if(last_changes != current_changes):
                        process.terminate()
                        outfile.close()
                        remove(str(pid) + ".out")
                        has_errored = True
                        break
        else:
            program = load_program_from_file(args.filename)
            compile_program_linux_x86_64(program, args.output, args.debug)
            compile_assembly(args.output, args.debug)
        if args.time:
            compilation_end = datetime.now().timestamp()
            compilation_took = compilation_end - start_timestamp
            print(
                'compilation finished, took'
                f' {compilation_took:.3f}sec\n')
