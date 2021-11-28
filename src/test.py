import json
import subprocess
import datetime
import sys

test_pi = 'pi' in sys.argv
test_pc = 'pc' in sys.argv

if test_pi:
    print("PI = python interpretation mode")

if test_pc:
    print("PC = python compilation mode\n")

tests = json.loads(open("./tests/_tests.json").read())

max_desc_length = max(
    max(list(map(lambda x: len(x['description']), tests))), 13)

print(
    f"┌{'────┬─────────┬' if test_pi else ''}{'────┬─────────┬' if test_pc else ''}──────────────────┬{'─' * (max_desc_length + 2)}┐")
print(
    f"│{' PI │ PI perf │' if test_pi else ''}{' PC │ PC perf │' if test_pc else ''} test             │ description {' ' * (max_desc_length - 11)}│")
print(
    f"├{'────┼─────────┼' if test_pi else ''}{'────┼─────────┼' if test_pc else ''}──────────────────┼{'─' * (max_desc_length + 2)}┤")

failed_tests = []

python_executable = "python3" if sys.platform == "linux" else "python"

for test in tests:
    testname = test['test']
    description = test['description']
    expected_result = test['expected']

    pi_errors = []
    pc_errors = []
    pi_results = ""
    pi_unix_start = 0
    pi_unix_end = 0
    pc_results = ""
    pc_unix_start = 0
    pc_unix_end = 0
    compilation_succeeded = True
    interpretation_succeeded = True

    if test_pi:
        try:
            pi_unix_start = datetime.datetime.now().timestamp()

            # Interpret the script
            result = subprocess.run(
                [python_executable, 'bcs.py', f'./tests/{testname}.bcs', '-i'],
                capture_output=True)

            pi_unix_end = datetime.datetime.now().timestamp()

            # See if it was successfull
            interpretation_succeeded = result.stdout.decode(
                'utf-8').replace('\r', '') == expected_result

            # Save the results
            pi_results = result.stdout.decode('utf-8').replace('\r', '')

        except FileNotFoundError as e:
            pc_errors.append("File not found:"+e.filename)
            interpretation_succeeded = False
            pi_unix_end = 0
            pi_unix_start = 0

        except Exception as e:
            pi_errors.append("Unhandled exception")
            pi_errors.append(e)
            interpretation_succeeded = False
            pi_unix_end = 0
            pi_unix_start = 0

        # Print the PI result
        print(
            f"│ {'  ' if interpretation_succeeded else 'X '} "
            f"│ {pi_unix_end - pi_unix_start:.3f}s  ", end='')

    if test_pc:
        # Compile the script
        try:
            subprocess.run(
                [python_executable, 'bcs.py',
                    f'./tests/{testname}.bcs', '-o',  f'./tests/{testname}'],
                capture_output=True)

            pc_unix_start = datetime.datetime.now().timestamp()

            # Run the compiled file
            print(f'./tests/{testname}')
            result = subprocess.run([f'./tests/{testname}'], capture_output=True)

            pc_unix_end = datetime.datetime.now().timestamp()

            # Save the results
            pc_results = result.stdout.decode('utf-8').replace('\r', '')

            # Delete the compiled file
            subprocess.run(['rm', f'./tests/{testname}'])

            # See if it was successfull
            compilation_succeeded = result.stdout.decode(
                'utf-8').replace('\r', '') == expected_result

        except FileNotFoundError as e:
            pc_errors.append("File not found:" + e.filename)
            compilation_succeeded = False
            pc_unix_end = 0
            pc_unix_start = 0

        except Exception as e:
            pc_errors.append("Unhandled exception")
            pc_errors.append(e)
        # Print the pc result

        print(
            f"│ {'  ' if compilation_succeeded else 'X '} "
            f"│ {pc_unix_end - pc_unix_start:.3f}s  ", end='')

    print(
        f'│ ./tests/{testname}.bcs │ {description}{" " * (max_desc_length - len(description))} │')

    buffer = f'error in ./tests/{testname}.bcs:\n'

    if not interpretation_succeeded:
        buffer += "\t----- interpretation mode -----\n"
        if(pi_unix_end == pi_unix_start == 0):
            buffer += "\ttest crashed:\n"
        for i in pi_errors:
            buffer += "\t" + i
        buffer += "\n"
        buffer += '\t' + pi_results.replace('\n', '\n\t') + '\n'

    if not compilation_succeeded:

        buffer += "\t----- compilation mode -----\n"
        if(pc_unix_end == pc_unix_start == 0):
            buffer += "\ttest crashed:\n"
        for i in pc_errors:
            buffer += "\t" + i
        buffer += "\n"
        buffer += '\t' + pc_results.replace('\n', '\n\t') + '\n'

    if not compilation_succeeded or not interpretation_succeeded:

        buffer += "\t----- expected result -----\n"
        buffer += '\t' + expected_result.replace('\n', '\n\t') + '\n'
        failed_tests.append(buffer)

print(
    f"└{'────┴─────────┴' if test_pi else ''}{'────┴─────────┴' if test_pc else ''}──────────────────┴{'─' * (max_desc_length + 2)}┘\n\n\n")

for failed_test in failed_tests:
    print(failed_test)
    print("\n")
