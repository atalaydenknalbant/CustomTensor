section .text
    global add_arrays
add_arrays:
    push rbx
    mov rbx, rcx
.loop:
    cmp rbx, 0
    je .done
    mov eax, [rsi]
    add eax, [rdx]
    mov [rdi], eax
    add rsi, 4
    add rdx, 4
    add rdi, 4
    dec rbx
    jmp .loop
.done:
    pop rbx
    ret

    global sub_arrays
sub_arrays:
    push rbx
    mov rbx, rcx
.loop_sub:
    cmp rbx, 0
    je .done_sub
    mov eax, [rsi]
    sub eax, [rdx]
    mov [rdi], eax
    add rsi, 4
    add rdx, 4
    add rdi, 4
    dec rbx
    jmp .loop_sub
.done_sub:
    pop rbx
    ret

    global mul_arrays
mul_arrays:
    push rbx
    mov rbx, rcx
.loop_mul:
    cmp rbx, 0
    je .done_mul
    mov eax, [rsi]
    imul eax, [rdx]
    mov [rdi], eax
    add rsi, 4
    add rdx, 4
    add rdi, 4
    dec rbx
    jmp .loop_mul
.done_mul:
    pop rbx
    ret

    global div_arrays
div_arrays:
    push rbx
    mov rbx, rcx
    mov r8, rdx
.loop_div:
    cmp rbx, 0
    je .done_div
    mov eax, [rsi]
    cdq
    idiv dword [r8]
    mov [rdi], eax
    add rsi, 4
    add r8, 4
    add rdi, 4
    dec rbx
    jmp .loop_div
.done_div:
    pop rbx
    ret
