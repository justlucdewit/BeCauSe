segment .text

; dump function
dump:
    mov     r9, -3689348814741910323
    sub     rsp, 40
    mov     BYTE [rsp+31], 10
    lea     rcx, [rsp+30]

.L2:
    mov     rax, rdi
    lea     r8, [rsp+32]
    mul     r9
    mov     rax, rdi
    sub     r8, rcx
    shr     rdx, 3
    lea     rsi, [rdx+rdx*4]
    add     rsi, rsi
    sub     rax, rsi
    add     eax, 48
    mov     BYTE [rcx], al
    mov     rax, rdi
    mov     rdi, rdx
    mov     rdx, rcx
    sub     rcx, 1
    cmp     rax, 9
    ja      .L2
    lea     rax, [rsp+32]
    mov     edi, 1
    sub     rdx, rax
    xor     eax, eax
    lea     rsi, [rsp+32+rdx]
    mov     rdx, r8
    mov     rax, 1
    syscall
    add     rsp, 40
    ret

global _start
_start:

addr_0: ; (PUSH 5)
    push 5

addr_1: ; (PUSH 6)
    push 6

addr_2: ; (GREATER)
    mov rcx, 0
    mov rdx, 1
    pop rbx
    pop rax
    cmp rax, rbx
    cmovg rcx, rdx
    push rcx

addr_3: ; (PRINT)
    pop rdi
    call dump

addr_4: ; (PUSH 6)
    push 6

addr_5: ; (PUSH 5)
    push 5

addr_6: ; (GREATER)
    mov rcx, 0
    mov rdx, 1
    pop rbx
    pop rax
    cmp rax, rbx
    cmovg rcx, rdx
    push rcx

addr_7: ; (PRINT)
    pop rdi
    call dump

addr_8: ; Exit program with code 0
    mov rax, 60
    mov rdi, 0
    syscall
    ret



segment .bss
mem: resb 640000