#!/usr/bin/env python3
import sys
from modules.usage import *
from modules.run_program import *
from modules.compile_program import *
from modules.opcodes import *
import subprocess

def uncons(xs):
    return (xs[0], xs[1:])

def parse_word(word):
    if word == '+':
        return (OP_ADD, )
    elif word == '-':
        return (OP_SUBTRACT, )
    elif word == '.':
        return (OP_PRINT, )
    else:
        return (OP_PUSH, int(word))

def load_program_from_file(input_file_name):
    with open(input_file_name, "r") as f:
        words = f.read().split()
        return [parse_word(word) for word in words]


if __name__ == "__main__":
    (program_name, argv) = uncons(sys.argv)

    if len(argv) < 1:
        usage(program_name)
        print("ERROR: no subcommand provided\n")
        exit(-1)

    (subcommand, options) = uncons(argv)
    
    debug = "debug" in options

    if (subcommand == "help"):
        if len(options) < 1:
            usage(program_name)
    elif (subcommand == "run"):
        if len(options) < 1:
            usage(program_name)
            print("ERROR: no filename given\n")
            exit(-1)

        (input_file_name, options) = uncons(options)
        program = load_program_from_file(input_file_name)
        run_program(program)
    elif (subcommand == "com"):
        if len(options) < 1:
            usage(program_name)
            print("ERROR: no filename given\n")
            exit(-1)

        (input_file_name, options) = uncons(options)
        program = load_program_from_file(input_file_name)
        compile_program(program, "output.asm")
        subprocess.call(["nasm", "-felf64", "output.asm"])
        subprocess.call(["ld", "-o", "output", "output.o"])
        subprocess.call(["rm", "output.o"])

        if not debug:
            subprocess.call(["rm", "output.asm"])
    else:
        print(f"ERROR: no subcommand like '{subcommand}'")