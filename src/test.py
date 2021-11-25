import json
import subprocess

print("pi = python interpretation mode")
print("pc = python compilation mode\n")

print("| pi | pc | test name")

tests = json.loads(open("./tests/_tests.json").read())

for test in tests:
    testname = test['test']
    expected_result = test['expected']

    result = subprocess.run(
        ['python', 'bcs.py', f'./tests/{testname}.bcs', '-i'],
        capture_output=True)

    interpretation_succeeded = result.stdout.decode(
        'utf-8').replace('\r', '') == expected_result

    print(f"| {'🟢' if interpretation_succeeded else '🔴'} |    | {testname}")
