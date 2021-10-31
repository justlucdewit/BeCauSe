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

        for ip in range(len(program)):
            opcode = program[ip]

            output.write(f"addr_{ip}: ; ({instructions_map[opcode[0]]}{' ' + str(opcode[1]) if len(opcode) > 1 else ''})\n")
            
            if opcode[0] == OP_PUSH:
                output.write(f"    push {opcode[1]}\n\n")

            elif opcode[0] == OP_DUP:
                output.write(f"    pop rax\n")
                output.write(f"    push rax\n")
                output.write(f"    push rax\n\n")

            elif opcode[0] == OP_2DUP:
                output.write(f"    pop rax\n")
                output.write(f"    pop rbx\n")
                output.write(f"    push rbx\n")
                output.write(f"    push rax\n")
                output.write(f"    push rbx\n")
                output.write(f"    push rax\n\n")

            elif opcode[0] == OP_DROP:
                output.write(f"    pop rax\n\n")

            elif opcode[0] == OP_ADD:
                output.write(f"    pop rax\n")
                output.write(f"    pop rbx\n")
                output.write(f"    add rax, rbx\n")
                output.write(f"    push rax\n\n")
            
            elif opcode[0] == OP_SUBTRACT:
                output.write(f"    pop rbx\n")
                output.write(f"    pop rax\n")
                output.write(f"    sub rax, rbx\n")
                output.write(f"    push rax\n\n")

            elif opcode[0] == OP_PRINT:
                output.write(f"    pop rdi\n")
                output.write(f"    call dump\n\n")

            elif opcode[0] == OP_GREATER:
                output.write(f"    mov rcx, 0\n")
                output.write(f"    mov rdx, 1\n")
                output.write(f"    pop rbx\n")
                output.write(f"    pop rax\n")
                output.write(f"    cmp rax, rbx\n")
                output.write(f"    cmovg rcx, rdx\n")
                output.write(f"    push rcx\n\n")

            elif opcode[0] == OP_SMALLER:
                output.write(f"    mov rcx, 0\n")
                output.write(f"    mov rdx, 1\n")
                output.write(f"    pop rbx\n")
                output.write(f"    pop rax\n")
                output.write(f"    cmp rax, rbx\n")
                output.write(f"    cmovl rcx, rdx\n")
                output.write(f"    push rcx\n\n")

            elif opcode[0] == OP_EQUAL:
                output.write(f"    mov rcx, 0\n")
                output.write(f"    mov rdx, 1\n")
                output.write(f"    pop rax\n")
                output.write(f"    pop rbx\n")
                output.write(f"    cmp rax, rbx\n")
                output.write(f"    cmove rcx, rdx\n")
                output.write(f"    push rcx\n\n")

            elif opcode[0] == OP_IF:
                output.write(f"    pop rax\n")
                output.write(f"    test rax, rax\n")
                output.write(f"    jz addr_{opcode[1]}\n\n")

            elif opcode[0] == OP_ELSE:
                output.write(f"    jmp addr_{opcode[1]}\n\n")

            elif opcode[0] == OP_END:
                if ip + 1 != opcode[1]:
                    output.write(f"    jmp addr_{opcode[1]}\n\n")

            elif opcode[0] == OP_WHILE:
                output.write(f"\n")

            elif opcode[0] == OP_DO:
                output.write(f"    pop rax\n")
                output.write(f"    test rax, rax\n")
                output.write(f"    jz addr_{opcode[1]}\n\n")
            
            elif opcode[0] == OP_MEM:
                output.write(f"    push mem\n\n")
            
            elif opcode[0] == OP_LOAD:
                output.write(f"    pop rax\n")
                output.write(f"    xor rbx, rbx\n")
                output.write(f"    mov bl, [rax]\n")
                output.write(f"    push rbx\n\n")

            elif opcode[0] == OP_STORE:
                output.write(f"    pop rax\n")
                output.write(f"    pop rbx\n")
                output.write(f"    mov [rbx], al\n\n")

            elif opcode[0] == OP_SYSCALL0:
                output.write(f"    pop rax\n")
                output.write(f"    syscall\n\n")

            elif opcode[0] == OP_SYSCALL1:
                output.write(f"    pop rax\n")
                output.write(f"    pop rdi\n")
                output.write(f"    syscall\n\n")

            elif opcode[0] == OP_SYSCALL2:
                output.write(f"    pop rax\n")
                output.write(f"    pop rdi\n")
                output.write(f"    pop rsi\n")
                output.write(f"    syscall\n\n")

            elif opcode[0] == OP_SYSCALL3:
                output.write(f"    pop rax\n")
                output.write(f"    pop rdi\n")
                output.write(f"    pop rsi\n")
                output.write(f"    pop rdx\n")
                output.write(f"    syscall\n\n")

            elif opcode[0] == OP_SYSCALL4:
                output.write(f"    pop rax\n")
                output.write(f"    pop rdi\n")
                output.write(f"    pop rsi\n")
                output.write(f"    pop rdx\n")
                output.write(f"    pop r10\n")
                output.write(f"    syscall\n\n")

            elif opcode[0] == OP_SYSCALL5:
                output.write(f"    pop rax\n")
                output.write(f"    pop rdi\n")
                output.write(f"    pop rsi\n")
                output.write(f"    pop rdx\n")
                output.write(f"    pop r10\n")
                output.write(f"    pop r8\n")
                output.write(f"    syscall\n\n")

            elif opcode[0] == OP_SYSCALL6:
                output.write(f"    pop rax\n")
                output.write(f"    pop rdi\n")
                output.write(f"    pop rsi\n")
                output.write(f"    pop rdx\n")
                output.write(f"    pop r10\n")
                output.write(f"    pop r8\n")
                output.write(f"    pop r9\n")
                output.write(f"    syscall\n\n")

            else:
                print("Compile Error: Unknown opcode encountered in compile_program()")
                exit(-1)

        output.write(f"addr_{len(program)}: ; Exit program with code 0\n")
        output.write("    mov rax, 60\n")
        output.write("    mov rdi, 0\n")
        output.write("    syscall\n")
        output.write("    ret")

        # Create memory segment
        output.write("\n\nsegment .bss\n")
        output.write(f"mem: resb {MEMORY_CAPACITY}")