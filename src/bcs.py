#!/usr/bin/env python3

from modules.run_program import *
from modules.compile_program import *
from modules.opcodes import *
from modules.parser import *

import sys
import subprocess
import argparse

# arg_parser.print_help()

BCS_VERSION = "BCS Compiler/Interpreter V1.0.0"

arg_parser = argparse.ArgumentParser(description='BeCause programming language compiler and interpreter')

sysargs = sys.argv[1:]

arg_parser.add_argument('filename', nargs='?', help='File with the source code to compile/interpret', default='')
arg_parser.add_argument('-v', '--version', help='Show the version of this BCS installation', action='store_true')
arg_parser.add_argument('-d', '--debug', help='Prevent deletion of output .asm file', action='store_true')
arg_parser.add_argument('-r', '--run', help='Run the produced executable after compilation', action='store_true')
arg_parser.add_argument('-i', '--interpret', help='Interpret the program in build-in interpreter instead of compiling it', action='store_true')
arg_parser.add_argument("-o", "--output", metavar='<file>', help="Directs the output to a name of your choice")

args = arg_parser.parse_args(sysargs)

if not args.debug and not args.interpret and not args.run and not args.version and args.output == None:
    print("test")
    arg_parser.print_help()
    exit(0)

if args.version:
    print(BCS_VERSION)
    exit(0)


if __name__ == "__main__":
    if args.interpret:
        program = load_program_from_file(args.filename)
        run_program(program)

    # elif subcommand == "com":
    #     if len(options) < 1:
    #         usage(program_name)
    #         print("CLI Error: no filename given\n")
    #         exit(-1)

    #     (input_file_name, options) = uncons(options)
    #     program = load_program_from_file(input_file_name)
    #     compile_program_linux_x86_64(program, "output.asm")
    #     subprocess.call(["nasm", "-felf64", "output.asm"])
    #     subprocess.call(["ld", "-o", "output", "output.o"])
    #     subprocess.call(["rm", "output.o"])

    #     if not args.debug:
    #         subprocess.call(["rm", "output.asm"])
