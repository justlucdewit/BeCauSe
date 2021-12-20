# Import standard libraries
import argparse
import sys

# Create the parser
arg_parser = argparse.ArgumentParser(
    description='BeCause programming language compiler and interpreter')

# List the possible program arguments
arg_parser.add_argument(
    '-v', '--version',
    help='Show the version of this BCS installation',
    action='store_true')

arg_parser.add_argument(
    '-d',
    '--debug',
    help='Prevent deletion of output .asm file',
    action='store_true')

arg_parser.add_argument(
    '-r',
    '--run',
    help='Run the produced executable after compilation',
    action='store_true')

arg_parser.add_argument(
    '-i',
    '--interpret',
    help='Interpret the program instead of compiling it',
    action='store_true')

arg_parser.add_argument(
    'filename',
    nargs='?',
    help='File with the source code to compile/interpret',
    default='')

arg_parser.add_argument(
    "-o",
    "--output",
    metavar='<file>',
    help="Directs the output to a name of your choice")

arg_parser.add_argument(
    '-t', '--time',
    help='Time how long compilation/interpretation took',
    action='store_true')

# Actually parse the arguments
args, rest_args = arg_parser.parse_known_args()

rest_args = [sys.argv[0]] + rest_args
