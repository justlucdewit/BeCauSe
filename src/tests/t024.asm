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

addr_0: ; (PUSH 1)
    push 1

addr_1: ; (PUSH 2)
    push 2

addr_2: ; (PUSH 3)
    push 3

addr_3: ; (ROT)
    pop rax
    pop rbx
    pop rcx
    push rbx
    push rax
    push rcx

addr_4: ; (PRINT)
    pop rdi
    call dump

addr_5: ; (PRINT)
    pop rdi
    call dump

addr_6: ; (PRINT)
    pop rdi
    call dump

addr_7: ; Exit program with code 0
    mov rax, 60
    mov rdi, 0
    syscall
    ret



segment .bss
mem: resb 640000