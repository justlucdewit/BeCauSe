from modules.opcodes import *

def compile_program(program, out_file_path):
    with open(out_file_path, "w+") as output:
        # text segment
        output.write("segment .text\n\n")

        # print function
        output.write("; dump function\n")
        output.write("dump:\n")
        output.write("    mov     r9, -3689348814741910323\n")
        output.write("    sub     rsp, 40\n")
        output.write("    mov     BYTE [rsp+31], 10\n")
        output.write("    lea     rcx, [rsp+30]\n")
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
        output.write("_start:\n")

        for opcode in program:
            if opcode[0] == OP_PUSH:
                output.write(f"    ; push {opcode[1]}\n")
                output.write(f"    push {opcode[1]}\n\n")
            elif opcode[0] == OP_ADD:
                output.write(f"    ; add\n")
                output.write(f"    pop rax\n")
                output.write(f"    pop rbx\n")
                output.write(f"    add rax, rbx\n")
                output.write(f"    push rax\n\n")
            elif opcode[0] == OP_PRINT:
                output.write(f"    ; print\n")
                output.write(f"    pop rdi\n")
                output.write(f"    call dump\n\n")
            else:
                assert False, "unreachable"

        output.write("    ; exit the program with code 0\n")
        output.write("    mov rax, 60\n")
        output.write("    mov rdi, 0\n")
        output.write("    syscall\n")
        output.write("    ret")