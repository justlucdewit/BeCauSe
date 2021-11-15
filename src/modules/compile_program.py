# Import standard libraries
import subprocess

# Import custom modules
from modules.opcodes import (MEMORY_CAPACITY, OP_2DUP, OP_ADD, OP_BITWISE_AND,
                             OP_BITWISE_OR, OP_DO, OP_DROP, OP_DUP, OP_ELSE,
                             OP_END, OP_EQUAL, OP_GREATER, OP_IF, OP_LOAD,
                             OP_MEM, OP_MULTIPLY, OP_OVER, OP_PRINT,
                             OP_PUSH_STRING, OP_SHIFT_LEFT, OP_SHIFT_RIGHT,
                             OP_SMALLER, OP_STORE, OP_SUBTRACT, OP_SWAP,
                             OP_SYSCALL0, OP_SYSCALL1, OP_SYSCALL2,
                             OP_SYSCALL3, OP_SYSCALL4, OP_SYSCALL5,
                             OP_SYSCALL6, OP_WHILE, instructions_map, OP_PUSH)


def compile_program_linux_x86_64(program, out_file_path, debug):
    output_asm_name = "output.asm" if out_file_path is None else out_file_path + ".asm"

    with open(output_asm_name, "w+") as output:
        # text segment
        output.write("segment .text\n\n")

        # print function
        output.write("; dump function\n")
        output.write("dump:\n")
        output.write("    mov     r9, -3689348814741910323\n")
        output.write("    sub     rsp, 40\n")
        output.write("    mov     BYTE [rsp+31], 10\n")
        output.write("    lea     rcx, [rsp+30]\n\n")
        output.write(".L2:\n")
        output.write("    mov     rax, rdi\n")
        output.write("    lea     r8, [rsp+32]\n")
        output.write("    mul     r9\n")
        output.write("    mov     rax, rdi\n")
        output.write("    sub     r8, rcx\n")
        output.write("    shr     rdx, 3\n")
        output.write("    lea     rsi, [rdx+rdx*4]\n")
        output.write("    add     rsi, rsi\n")
        output.write("    sub     rax, rsi\n")
        output.write("    add     eax, 48\n")
        output.write("    mov     BYTE [rcx], al\n")
        output.write("    mov     rax, rdi\n")
        output.write("    mov     rdi, rdx\n")
        output.write("    mov     rdx, rcx\n")
        output.write("    sub     rcx, 1\n")
        output.write("    cmp     rax, 9\n")
        output.write("    ja      .L2\n")
        output.write("    lea     rax, [rsp+32]\n")
        output.write("    mov     edi, 1\n")
        output.write("    sub     rdx, rax\n")
        output.write("    xor     eax, eax\n")
        output.write("    lea     rsi, [rsp+32+rdx]\n")
        output.write("    mov     rdx, r8\n")
        output.write("    mov     rax, 1\n")
        output.write("    syscall\n")
        output.write("    add     rsp, 40\n")
        output.write("    ret\n\n")

        # start the start
        output.write("global _start\n")
        output.write("_start:\n\n")

        strings = []

        for op in program:
            if op['type'] == OP_PUSH_STRING:
                op['string_id'] = f"string_literal_{len(strings)}"
                strings.append(
                    {
                        "id": f"string_literal_{len(strings)}",
                        "data": op['value']
                    })

        for ip in range(len(program)):
            opcode = program[ip]

            instruction_value = ' ' + \
                str(opcode['value']).replace(
                    '\n', '\\n') if 'value' in opcode else ''

            output.write(
                f"addr_{ip}: ; ({instructions_map[opcode['type']]}" +
                f"{instruction_value})\n")

            if opcode['type'] == OP_PUSH:
                output.write(f"    push {opcode['value']}\n\n")

            elif opcode['type'] == OP_PUSH_STRING:
                string_length = len(
                    list(filter(
                        lambda x: x['id'] == opcode['string_id'], strings
                    ))[0]['data'])
                output.write(f"    push {string_length}\n")
                output.write(f"    push {opcode['string_id']}\n\n")

            elif opcode['type'] == OP_DUP:
                output.write("    pop rax\n")
                output.write("    push rax\n")
                output.write("    push rax\n\n")

            elif opcode['type'] == OP_2DUP:
                output.write("    pop rax\n")
                output.write("    pop rbx\n")
                output.write("    push rbx\n")
                output.write("    push rax\n")
                output.write("    push rbx\n")
                output.write("    push rax\n\n")

            elif opcode['type'] == OP_DROP:
                output.write("    pop rax\n\n")

            elif opcode['type'] == OP_SWAP:
                output.write("    pop rax\n")
                output.write("    pop rbx\n")
                output.write("    push rax\n")
                output.write("    push rbx\n\n")

            elif opcode['type'] == OP_OVER:
                output.write("    pop rax\n")
                output.write("    pop rbx\n")
                output.write("    push rbx\n")
                output.write("    push rax\n")
                output.write("    push rbx\n")

            elif opcode['type'] == OP_ADD:
                output.write("    pop rax\n")
                output.write("    pop rbx\n")
                output.write("    add rax, rbx\n")
                output.write("    push rax\n\n")

            elif opcode['type'] == OP_SUBTRACT:
                output.write("    pop rbx\n")
                output.write("    pop rax\n")
                output.write("    sub rax, rbx\n")
                output.write("    push rax\n\n")

            elif opcode['type'] == OP_MULTIPLY:
                output.write("    pop rax\n")
                output.write("    pop rbx\n")
                output.write("    mul rbx\n")
                output.write("    push rax\n\n")

            elif opcode['type'] == OP_SHIFT_LEFT:
                output.write("    pop rcx\n")
                output.write("    pop rbx\n")
                output.write("    shl rbx, cl\n")
                output.write("    push rbx\n\n")

            elif opcode['type'] == OP_SHIFT_RIGHT:
                output.write("    pop rcx\n")
                output.write("    pop rbx\n")
                output.write("    shr rbx, cl\n")
                output.write("    push rbx\n\n")

            elif opcode['type'] == OP_BITWISE_AND:
                output.write("    pop rax\n")
                output.write("    pop rbx\n")
                output.write("    and rbx, rax\n")
                output.write("    push rbx\n\n")

            elif opcode['type'] == OP_BITWISE_OR:
                output.write("    pop rax\n")
                output.write("    pop rbx\n")
                output.write("    or rbx, rax\n")
                output.write("    push rbx\n\n")

            elif opcode['type'] == OP_PRINT:
                output.write("    pop rdi\n")
                output.write("    call dump\n\n")

            elif opcode['type'] == OP_GREATER:
                output.write("    mov rcx, 0\n")
                output.write("    mov rdx, 1\n")
                output.write("    pop rbx\n")
                output.write("    pop rax\n")
                output.write("    cmp rax, rbx\n")
                output.write("    cmovg rcx, rdx\n")
                output.write("    push rcx\n\n")

            elif opcode['type'] == OP_SMALLER:
                output.write("    mov rcx, 0\n")
                output.write("    mov rdx, 1\n")
                output.write("    pop rbx\n")
                output.write("    pop rax\n")
                output.write("    cmp rax, rbx\n")
                output.write("    cmovl rcx, rdx\n")
                output.write("    push rcx\n\n")

            elif opcode['type'] == OP_EQUAL:
                output.write("    mov rcx, 0\n")
                output.write("    mov rdx, 1\n")
                output.write("    pop rax\n")
                output.write("    pop rbx\n")
                output.write("    cmp rax, rbx\n")
                output.write("    cmove rcx, rdx\n")
                output.write("    push rcx\n\n")

            elif opcode['type'] == OP_IF:
                output.write("    pop rax\n")
                output.write("    test rax, rax\n")
                output.write(f"    jz addr_{opcode['reference']}\n\n")

            elif opcode['type'] == OP_ELSE:
                output.write(f"    jmp addr_{opcode['reference']}\n\n")

            elif opcode['type'] == OP_END:
                if ip + 1 != opcode['reference']:
                    output.write(f"    jmp addr_{opcode['reference']}\n\n")

            elif opcode['type'] == OP_WHILE:
                output.write("\n")

            elif opcode['type'] == OP_DO:
                output.write("    pop rax\n")
                output.write("    test rax, rax\n")
                output.write("    jz addr_{opcode['reference']}\n\n")

            elif opcode['type'] == OP_MEM:
                output.write("    push mem\n\n")

            elif opcode['type'] == OP_LOAD:
                output.write("    pop rax\n")
                output.write("    xor rbx, rbx\n")
                output.write("    mov bl, [rax]\n")
                output.write("    push rbx\n\n")

            elif opcode['type'] == OP_STORE:
                output.write("    pop rax\n")
                output.write("    pop rbx\n")
                output.write("    mov [rbx], al\n\n")

            elif opcode['type'] == OP_SYSCALL0:
                output.write("    pop rax\n")
                output.write("    syscall\n\n")

            elif opcode['type'] == OP_SYSCALL1:
                output.write("    pop rax\n")
                output.write("    pop rdi\n")
                output.write("    syscall\n\n")

            elif opcode['type'] == OP_SYSCALL2:
                output.write("    pop rax\n")
                output.write("    pop rdi\n")
                output.write("    pop rsi\n")
                output.write("    syscall\n\n")

            elif opcode['type'] == OP_SYSCALL3:
                output.write("    pop rax\n")
                output.write("    pop rdi\n")
                output.write("    pop rsi\n")
                output.write("    pop rdx\n")
                output.write("    syscall\n\n")

            elif opcode['type'] == OP_SYSCALL4:
                output.write("    pop rax\n")
                output.write("    pop rdi\n")
                output.write("    pop rsi\n")
                output.write("    pop rdx\n")
                output.write("    pop r10\n")
                output.write("    syscall\n\n")

            elif opcode['type'] == OP_SYSCALL5:
                output.write("    pop rax\n")
                output.write("    pop rdi\n")
                output.write("    pop rsi\n")
                output.write("    pop rdx\n")
                output.write("    pop r10\n")
                output.write("    pop r8\n")
                output.write("    syscall\n\n")

            elif opcode['type'] == OP_SYSCALL6:
                output.write("    pop rax\n")
                output.write("    pop rdi\n")
                output.write("    pop rsi\n")
                output.write("    pop rdx\n")
                output.write("    pop r10\n")
                output.write("    pop r8\n")
                output.write("    pop r9\n")
                output.write("    syscall\n\n")

            else:
                print(
                    "Compile Error: Unknown opcode" +
                    " encountered in compile_program()")
                exit(-1)

        output.write(f"addr_{len(program)}: ; Exit program with code 0\n")
        output.write("    mov rax, 60\n")
        output.write("    mov rdi, 0\n")
        output.write("    syscall\n")
        output.write("    ret\n\n")

        if len(strings) > 0:
            output.write("section .data\n")
            for string in strings:
                string_bytes = ", ".join(
                    list(map(lambda x: str(ord(x)), list(string['data']))))
                output.write(f"    {string['id']}: db {string_bytes}\n")

        # Create memory segment
        output.write("\n\nsegment .bss\n")
        output.write(f"mem: resb {MEMORY_CAPACITY}")

    subprocess.call(["nasm", "-felf64", output_asm_name])

    subprocess.call(
        [
            "ld",
            "-o",
            args.output if args.output is not None else "output",
            args.output + '.o' if args.output is not None else 'output.o'
        ])

    subprocess.call(
        ["rm", args.output + '.o' if args.output is not None else 'output.o'])

    if not args.debug:
        subprocess.call(["rm", output_asm_name])
