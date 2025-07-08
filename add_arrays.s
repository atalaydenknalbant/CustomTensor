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

    global mod_arrays
mod_arrays:
    push rbx
    mov rbx, rcx
    mov r8, rdx
.loop_mod:
    cmp rbx, 0
    je .done_mod
    mov eax, [rsi]
    cdq
    idiv dword [r8]
    mov [rdi], edx
    add rsi, 4
    add r8, 4
    add rdi, 4
    dec rbx
    jmp .loop_mod
.done_mod:
    pop rbx
    ret

    global pow_arrays
pow_arrays:
    push rbx
    mov rbx, rcx
    mov r8, rdx
.loop_pow:
    cmp rbx, 0
    je .done_pow
    mov eax, [rsi]        ; base
    mov ecx, [r8]         ; exponent
    mov edx, 1            ; result
.pow_loop:
    cmp ecx, 0
    jle .store_pow
    imul edx, eax
    dec ecx
    jmp .pow_loop
.store_pow:
    mov [rdi], edx
    add rsi, 4
    add r8, 4
    add rdi, 4
    dec rbx
    jmp .loop_pow
.done_pow:
    pop rbx
    ret

    global sum_array
sum_array:
    push rbx
    xor eax, eax
    mov rbx, rsi
.loop_sum:
    cmp rbx, 0
    je .done_sum
    add eax, [rdi]
    add rdi, 4
    dec rbx
    jmp .loop_sum
.done_sum:
    pop rbx
    ret

    global dot_product
dot_product:
    push rbx
    xor eax, eax
    mov rbx, rdx
.loop_dot:
    cmp rbx, 0
    je .done_dot
    mov ecx, [rdi]
    imul ecx, dword [rsi]
    add eax, ecx
    add rdi, 4
    add rsi, 4
    dec rbx
    jmp .loop_dot
.done_dot:
    pop rbx
    ret
