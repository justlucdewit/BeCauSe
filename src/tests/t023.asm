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

addr_0: ; (PUSH 69)
    push 69

addr_1: ; (MEM)
    push mem

addr_2: ; (PUSH 0)
    push 0

addr_3: ; (ADD)
    pop rax
    pop rbx
    add rax, rbx
    push rax

addr_4: ; (STORE8)
    pop rax
    pop rbx
    mov [rax], bl

addr_5: ; (PUSH 987654567)
    push 987654567

addr_6: ; (MEM)
    push mem

addr_7: ; (PUSH 1)
    push 1

addr_8: ; (ADD)
    pop rax
    pop rbx
    add rax, rbx
    push rax

addr_9: ; (STORE32)
    pop rax
    pop rbx
    mov [rax], ebx

addr_10: ; (MEM)
    push mem

addr_11: ; (LOAD8)
    pop rax
    xor rbx, rbx
    mov bl, [rax]
    push rbx

addr_12: ; (PRINT)
    pop rdi
    call dump

addr_13: ; (MEM)
    push mem

addr_14: ; (PUSH 1)
    push 1

addr_15: ; (ADD)
    pop rax
    pop rbx
    add rax, rbx
    push rax

addr_16: ; (LOAD8)
    pop rax
    xor rbx, rbx
    mov bl, [rax]
    push rbx

addr_17: ; (PRINT)
    pop rdi
    call dump

addr_18: ; Exit program with code 0
    mov rax, 60
    mov rdi, 0
    syscall
    ret



segment .bss
mem: resb 640000