import json
import subprocess
import datetime
import sys

print("PI = python interpretation mode")
print("PC = python compilation mode\n")

tests = json.loads(open("./tests/_tests.json").read())

max_desc_length = max(
    max(list(map(lambda x: len(x['description']), tests))), 13)

print(
    f"┌────┬─────────┬────┬─────────┬──────────────────┬{'─' * max_desc_length}┐")
print("│ PI │ PI perf │ PC │ PC perf │ test             │ description │")
print(
    f"├────┼─────────┼────┼─────────┼──────────────────┼{'─' * max_desc_length}┤")

test_pi = 'pi' in sys.argv
test_pc = 'pc' in sys.argv

failed_tests = []


for test in tests:
    testname = test['test']
    expected_result = test['expected']

    pi_results = ""
    pi_unix_start = 0
    pi_unix_end = 0
    pc_results = ""
    pc_unix_start = 0
    pc_unix_end = 0
    compilation_succeeded = True
    interpretation_succeeded = True

    if test_pi:
        pi_unix_start = datetime.datetime.now().timestamp()

        # Interpret the script
        result = subprocess.run(
            ['python3', 'bcs.py', f'./tests/{testname}.bcs', '-i'],
            capture_output=True)

        pi_unix_end = datetime.datetime.now().timestamp()

        # See if it was successfull
        interpretation_succeeded = result.stdout.decode(
            'utf-8').replace('\r', '') == expected_result

        # Save the results
        pi_results = result.stdout.decode('utf-8').replace('\r', '')

        # Print the PI result
        print(
            f"│ {'🟢' if interpretation_succeeded else '🔴'} "
            f"{' ' if interpretation_succeeded else ''}", end=''
            f"│ {pi_unix_end - pi_unix_start:.3f}s  ")
    else:
        print("│ ❔ ", end='')

    if test_pc:
        # Compile the script
        subprocess.run(
            ['python3', 'bcs.py',
                f'./tests/{testname}.bcs', '-o',  f'./tests/{testname}'],
            capture_output=True)

        pc_unix_start = datetime.datetime.now().timestamp()

        # Run the compiled file
        result = subprocess.run([f'./tests/{testname}'], capture_output=True)

        pc_unix_end = datetime.datetime.now().timestamp()

        # Save the results
        pc_results = result.stdout.decode('utf-8').replace('\r', '')

        # Delete the compiled file
        subprocess.run(['rm', f'./tests/{testname}'])

        # See if it was successfull
        compilation_succeeded = result.stdout.decode(
            'utf-8').replace('\r', '') == expected_result

        # Print the pc result
        print(
            f"│ {'🟢' if compilation_succeeded else '🔴'} "
            f"{' ' if compilation_succeeded else ''}", end=''
            f"│ {pc_unix_end - pc_unix_start:.3f}s  ")

    else:
        print("│ ❔ ", end='')

    print(f'│ ./tests/{testname}.bcs │')

    buffer = f'error in ./tests/{testname}.bcs:\n'
    if not interpretation_succeeded:
        buffer += "\t----- interpretation mode -----\n"
        buffer += '\t' + pi_results.replace('\n', '\n\t') + '\n'

    if not compilation_succeeded:
        buffer += "\t----- compilation mode -----\n"
        buffer += '\t' + pc_results.replace('\n', '\n\t') + '\n'

    if not compilation_succeeded or not interpretation_succeeded:
        buffer += "\t----- expected result -----\n"
        buffer += '\t' + expected_result.replace('\n', '\n\t') + '\n'
        failed_tests.append(buffer)

print("└────┴─────────┴────┴─────────┴──────────────────┘\n\n\n")

for failed_test in failed_tests:
    print(failed_test)
    print("\n")
