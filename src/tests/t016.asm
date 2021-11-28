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

addr_0: ; (PUSH 15)
    push 15

addr_1: ; (PUSH 75)
    push 75

addr_2: ; (ADD)
    pop rax
    pop rbx
    add rax, rbx
    push rax

addr_3: ; (PUSH 1)
    push 1

addr_4: ; (GREATER)
    mov rcx, 0
    mov rdx, 1
    pop rbx
    pop rax
    cmp rax, rbx
    cmovg rcx, rdx
    push rcx

addr_5: ; (IF)
    pop rax
    test rax, rax
    jz addr_11

addr_6: ; (PUSH yep )
    push 4
    push string_literal_0

addr_7: ; (PUSH 1)
    push 1

addr_8: ; (PUSH 1)
    push 1

addr_9: ; (SYSCALL3)
    pop rax
    pop rdi
    pop rsi
    pop rdx
    syscall

addr_10: ; (ELSE)
    jmp addr_15

addr_11: ; (PUSH nope )
    push 5
    push string_literal_1

addr_12: ; (PUSH 1)
    push 1

addr_13: ; (PUSH 1)
    push 1

addr_14: ; (SYSCALL3)
    pop rax
    pop rdi
    pop rsi
    pop rdx
    syscall

addr_15: ; (END)
addr_16: ; (PUSH 15)
    push 15

addr_17: ; (PUSH 75)
    push 75

addr_18: ; (ADD)
    pop rax
    pop rbx
    add rax, rbx
    push rax

addr_19: ; (PUSH 1)
    push 1

addr_20: ; (SMALLER)
    mov rcx, 0
    mov rdx, 1
    pop rbx
    pop rax
    cmp rax, rbx
    cmovl rcx, rdx
    push rcx

addr_21: ; (IF)
    pop rax
    test rax, rax
    jz addr_27

addr_22: ; (PUSH yep\n)
    push 4
    push string_literal_2

addr_23: ; (PUSH 1)
    push 1

addr_24: ; (PUSH 1)
    push 1

addr_25: ; (SYSCALL3)
    pop rax
    pop rdi
    pop rsi
    pop rdx
    syscall

addr_26: ; (ELSE)
    jmp addr_31

addr_27: ; (PUSH nope\n)
    push 5
    push string_literal_3

addr_28: ; (PUSH 1)
    push 1

addr_29: ; (PUSH 1)
    push 1

addr_30: ; (SYSCALL3)
    pop rax
    pop rdi
    pop rsi
    pop rdx
    syscall

addr_31: ; (END)
addr_32: ; Exit program with code 0
    mov rax, 60
    mov rdi, 0
    syscall
    ret

section .data
    string_literal_0: db 121, 101, 112, 32
    string_literal_1: db 110, 111, 112, 101, 32
    string_literal_2: db 121, 101, 112, 10
    string_literal_3: db 110, 111, 112, 101, 10


segment .bss
mem: resb 640000