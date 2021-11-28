#!/usr/bin/env python3

# Import custom modules
import multiprocessing

from sys import stdout
from modules.compile_program import compile_assembly, compile_program_linux_x86_64
from modules.parser import load_program_from_file
from modules.repl import repl
from modules.run_program import run_program
from modules.argument_parser import args
from datetime import datetime
import os

from os import remove, stat
from time import sleep

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
        # program = load_program_from_file(args.filename)
        if args.watch:
            file_changes = False
            exit_program = False
            last_changes = stat(args.filename).st_mtime
            while(exit_program is False):
                program = load_program_from_file(args.filename)

                process = multiprocessing.Process(target=run_program,
                                                  args=[program])
                file_changes = False
                process.start()
                stdout = open(str(process.pid) + ".out", "w")

                while(file_changes is False and exit_program is False):
                    sleep(5)
                    if(process.is_alive() is False):
                        pid = process.pid
                        os.close(stdout.fileno())
                        remove(str(pid) + ".out")
                        exit_program = True
                    if(last_changes != stat(args.filename).st_mtime):
                        file_changes = True
                        pid = process.pid
                        process.terminate()
                        os.close(stdout.fileno())
                        remove(str(pid) + ".out")
                        last_changes = stat(args.filename).st_mtime

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
            file_changes = False
            exit_program = False
            last_changes = stat(args.filename).st_mtime
            while(exit_program is False):
                program = load_program_from_file(args.filename)
                compile_program_linux_x86_64(program, args.output, args.debug)
                process = multiprocessing.Process(target=compile_assembly,
                                                  args=[args.output, args.debug])
                stdout = open(str(process.pid) + ".out", "w")
                
                while(file_changes is False and exit_program is False):
                    sleep(5)
                    if(process.is_alive() is False):
                        pid = process.pid
                        os.close(stdout.fileno())
                        remove(str(pid) + ".out")
                        exit_program = True
                    if(last_changes != stat(args.filename).st_mtime):
                        file_changes = True
                        pid = process.pid
                        process.terminate()
                        os.close(stdout.fileno())
                        remove(str(pid) + ".out")
                        last_changes = stat(args.filename).st_mtime

        if args.time:
            compilation_end = datetime.now().timestamp()
            compilation_took = compilation_end - start_timestamp
            print(
                'compilation finished, took'
                f' {compilation_took:.3f}sec\n')
