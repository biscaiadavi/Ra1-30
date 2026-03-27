/* Gerado automaticamente — Fase 1 RPN → ARMv7 VFP — CPUlator DE1-SoC */
.syntax unified
.cpu cortex-a9
.fpu vfpv3-d16
.arm

.equ HEX3_HEX0, 0xFF200020
.equ HEX5_HEX4, 0xFF200030
.equ LEDR_BASE, 0xFF200000

.section .text
.global _start

_start:
	mrc p15, 0, r0, c1, c0, 2
	orr r0, r0, #0x300000
	mcr p15, 0, r0, c1, c0, 2
	isb
	mov r0, #0x40000000
	vmsr fpexc, r0
	ldr sp, =stack_top
	bl main_program
halt_loop:
	b halt_loop

/* Escreve parte baixa do IEEE754 em HEX3-0 (visualização no simulador) */
mostrar_d0_hex:
	push {r4, lr}
	sub sp, sp, #8
	vstr d0, [sp]
	ldr r0, [sp]
	ldr r4, =HEX3_HEX0
	str r0, [r4]
	add sp, sp, #8
	pop {r4, pc}

idiv_s32:
	push {r2-r7, lr}
	cmp r1, #0
	beq divzero_die
	mov r2, #0
	cmp r0, #0
	bge idiv_abs_divisor
	rsb r0, r0, #0
	eor r2, r2, #1
idiv_abs_divisor:
	cmp r1, #0
	bge idiv_prepare
	rsb r1, r1, #0
	eor r2, r2, #1
idiv_prepare:
	mov r4, #0
	mov r5, r0
	mov r6, r1
	mov r7, #1
idiv_align:
	cmp r6, r5
	bhi idiv_loop
	cmp r6, #0x40000000
	bhs idiv_loop
	lsl r6, r6, #1
	lsl r7, r7, #1
	b idiv_align
idiv_loop:
	cmp r7, #0
	beq idiv_apply_sign
	cmp r5, r6
	blo idiv_next
	sub r5, r5, r6
	orr r4, r4, r7
idiv_next:
	lsr r6, r6, #1
	lsr r7, r7, #1
	b idiv_loop
idiv_apply_sign:
	mov r0, r4
	cmp r2, #0
	beq idiv_ret
	rsb r0, r0, #0
idiv_ret:
	pop {r2-r7, pc}

main_program:
	push {r4-r11, lr}
	bl linha_0
	ldr r4, =hist
	mov r5, #0
	add r4, r4, r5
	vstr d0, [r4]
	bl mostrar_d0_hex
	bl linha_1
	ldr r4, =hist
	mov r5, #8
	add r4, r4, r5
	vstr d0, [r4]
	bl mostrar_d0_hex
	bl linha_2
	ldr r4, =hist
	mov r5, #16
	add r4, r4, r5
	vstr d0, [r4]
	bl mostrar_d0_hex
	bl linha_3
	ldr r4, =hist
	mov r5, #24
	add r4, r4, r5
	vstr d0, [r4]
	bl mostrar_d0_hex
	bl linha_4
	ldr r4, =hist
	mov r5, #32
	add r4, r4, r5
	vstr d0, [r4]
	bl mostrar_d0_hex
	bl linha_5
	ldr r4, =hist
	mov r5, #40
	add r4, r4, r5
	vstr d0, [r4]
	bl mostrar_d0_hex
	bl linha_6
	ldr r4, =hist
	mov r5, #48
	add r4, r4, r5
	vstr d0, [r4]
	bl mostrar_d0_hex
	bl linha_7
	ldr r4, =hist
	mov r5, #56
	add r4, r4, r5
	vstr d0, [r4]
	bl mostrar_d0_hex
	bl linha_8
	ldr r4, =hist
	mov r5, #64
	add r4, r4, r5
	vstr d0, [r4]
	bl mostrar_d0_hex
	bl linha_9
	ldr r4, =hist
	mov r5, #72
	add r4, r4, r5
	vstr d0, [r4]
	bl mostrar_d0_hex
	bl linha_10
	ldr r4, =hist
	mov r5, #80
	add r4, r4, r5
	vstr d0, [r4]
	bl mostrar_d0_hex
	bl linha_11
	ldr r4, =hist
	mov r5, #88
	add r4, r4, r5
	vstr d0, [r4]
	bl mostrar_d0_hex
	pop {r4-r11, pc}

linha_0:
	push {lr}
	ldr r0, =lit_12_0
	vldr d0, [r0]
	vpush {d0}
	ldr r0, =lit_4_0
	vldr d0, [r0]
	vpop {d1}
	vdiv.f64 d0, d1, d0
	vpush {d0}
	ldr r0, =lit_3_0
	vldr d0, [r0]
	vpush {d0}
	ldr r0, =lit_3_0
	vldr d0, [r0]
	vpop {d1}
	vmul.f64 d0, d1, d0
	vpop {d1}
	vsub.f64 d0, d1, d0
	pop {pc}

linha_1:
	push {lr}
	ldr r0, =lit_15_0
	vldr d0, [r0]
	vpush {d0}
	ldr r0, =lit_4_0
	vldr d0, [r0]
	vpop {d1}
	vcvt.s32.f64 s0, d1
	vcvt.s32.f64 s2, d0
	vmov r0, s0
	vmov r1, s2
	cmp r1, #0
	beq divzero_die
	bl idiv_s32
	vmov s4, r0
	vcvt.f64.s32 d0, s4
	vpush {d0}
	ldr r0, =lit_15_0
	vldr d0, [r0]
	vpush {d0}
	ldr r0, =lit_4_0
	vldr d0, [r0]
	vpop {d1}
	vcvt.s32.f64 s0, d1
	vcvt.s32.f64 s2, d0
	vmov r0, s0
	vmov r1, s2
	cmp r1, #0
	beq divzero_die
	push {r0, r1}
	bl idiv_s32
	pop {r2, r3}
	mul r1, r0, r3
	sub r12, r2, r1
	vmov s4, r12
	vcvt.f64.s32 d0, s4
	vpop {d1}
	vadd.f64 d0, d1, d0
	pop {pc}

linha_2:
	push {lr}
	ldr r0, =lit_2_0
	vldr d0, [r0]
	vpush {d0}
	ldr r0, =lit_10_0
	vldr d0, [r0]
	vpop {d1}
	vcvt.s32.f64 s4, d0
	vmov r2, s4
	cmp r2, #0
	blt pow_neg_err
	beq pow_z_1
	cmp r2, #1
	ble pow_one_2
	vmov.f64 d3, d1
	mov r12, r2
	subs r12, r12, #1
pow_lp_4:
	vmul.f64 d3, d3, d1
	subs r12, r12, #1
	bne pow_lp_4
	vmov.f64 d0, d3
	b pow_fin_3
pow_one_2:
	vmov.f64 d0, d1
	b pow_fin_3
pow_z_1:
	ldr r0, =lit_one
	vldr d0, [r0]
pow_fin_3:
	nop
	vpush {d0}
	ldr r0, =hist
	mov r1, #8
	add r0, r0, r1
	vldr d0, [r0]
	vpop {d1}
	vsub.f64 d0, d1, d0
	pop {pc}

linha_3:
	push {lr}
	ldr r0, =lit_7_0
	vldr d0, [r0]
	ldr r0, =mem_BUFFER
	vstr d0, [r0]
	vpush {d0}
	ldr r0, =mem_BUFFER
	vldr d0, [r0]
	vpush {d0}
	ldr r0, =lit_2_0
	vldr d0, [r0]
	vpush {d0}
	ldr r0, =lit_1_0
	vldr d0, [r0]
	vpop {d1}
	vadd.f64 d0, d1, d0
	vpop {d1}
	vadd.f64 d0, d1, d0
	vpop {d1}
	vmul.f64 d0, d1, d0
	pop {pc}

linha_4:
	push {lr}
	ldr r0, =lit_100_0
	vldr d0, [r0]
	vpush {d0}
	ldr r0, =lit_50_0
	vldr d0, [r0]
	vpop {d1}
	vadd.f64 d0, d1, d0
	vpush {d0}
	ldr r0, =lit_25_0
	vldr d0, [r0]
	vpush {d0}
	ldr r0, =lit_5_0
	vldr d0, [r0]
	vpop {d1}
	vdiv.f64 d0, d1, d0
	vpop {d1}
	vmul.f64 d0, d1, d0
	pop {pc}

linha_5:
	push {lr}
	ldr r0, =lit_1_0
	vldr d0, [r0]
	vpush {d0}
	ldr r0, =lit_1_0
	vldr d0, [r0]
	vpop {d1}
	vadd.f64 d0, d1, d0
	vpush {d0}
	ldr r0, =lit_2_0
	vldr d0, [r0]
	vpush {d0}
	ldr r0, =lit_2_0
	vldr d0, [r0]
	vpop {d1}
	vadd.f64 d0, d1, d0
	vpop {d1}
	vsub.f64 d0, d1, d0
	vpush {d0}
	ldr r0, =lit_3_0
	vldr d0, [r0]
	vpush {d0}
	ldr r0, =lit_3_0
	vldr d0, [r0]
	vpop {d1}
	vadd.f64 d0, d1, d0
	vpop {d1}
	vsub.f64 d0, d1, d0
	pop {pc}

linha_6:
	push {lr}
	ldr r0, =lit_64_0
	vldr d0, [r0]
	vpush {d0}
	ldr r0, =lit_8_0
	vldr d0, [r0]
	vpop {d1}
	vcvt.s32.f64 s0, d1
	vcvt.s32.f64 s2, d0
	vmov r0, s0
	vmov r1, s2
	cmp r1, #0
	beq divzero_die
	bl idiv_s32
	vmov s4, r0
	vcvt.f64.s32 d0, s4
	vpush {d0}
	ldr r0, =lit_2_0
	vldr d0, [r0]
	vpush {d0}
	ldr r0, =lit_3_0
	vldr d0, [r0]
	vpop {d1}
	vcvt.s32.f64 s4, d0
	vmov r2, s4
	cmp r2, #0
	blt pow_neg_err
	beq pow_z_5
	cmp r2, #1
	ble pow_one_6
	vmov.f64 d3, d1
	mov r12, r2
	subs r12, r12, #1
pow_lp_8:
	vmul.f64 d3, d3, d1
	subs r12, r12, #1
	bne pow_lp_8
	vmov.f64 d0, d3
	b pow_fin_7
pow_one_6:
	vmov.f64 d0, d1
	b pow_fin_7
pow_z_5:
	ldr r0, =lit_one
	vldr d0, [r0]
pow_fin_7:
	nop
	vpop {d1}
	vadd.f64 d0, d1, d0
	pop {pc}

linha_7:
	push {lr}
	ldr r0, =lit_9_0
	vldr d0, [r0]
	vpush {d0}
	ldr r0, =lit_5_0
	vldr d0, [r0]
	vpop {d1}
	vcvt.s32.f64 s0, d1
	vcvt.s32.f64 s2, d0
	vmov r0, s0
	vmov r1, s2
	cmp r1, #0
	beq divzero_die
	push {r0, r1}
	bl idiv_s32
	pop {r2, r3}
	mul r1, r0, r3
	sub r12, r2, r1
	vmov s4, r12
	vcvt.f64.s32 d0, s4
	vpush {d0}
	ldr r0, =lit_2_0
	vldr d0, [r0]
	vpush {d0}
	ldr r0, =lit_1_0
	vldr d0, [r0]
	vpop {d1}
	vadd.f64 d0, d1, d0
	vpop {d1}
	vmul.f64 d0, d1, d0
	pop {pc}

linha_8:
	push {lr}
	ldr r0, =lit_11_0
	vldr d0, [r0]
	vpush {d0}
	ldr r0, =lit_3_0
	vldr d0, [r0]
	vpop {d1}
	vcvt.s32.f64 s0, d1
	vcvt.s32.f64 s2, d0
	vmov r0, s0
	vmov r1, s2
	cmp r1, #0
	beq divzero_die
	bl idiv_s32
	vmov s4, r0
	vcvt.f64.s32 d0, s4
	vpush {d0}
	ldr r0, =lit_11_0
	vldr d0, [r0]
	vpush {d0}
	ldr r0, =lit_3_0
	vldr d0, [r0]
	vpop {d1}
	vcvt.s32.f64 s0, d1
	vcvt.s32.f64 s2, d0
	vmov r0, s0
	vmov r1, s2
	cmp r1, #0
	beq divzero_die
	push {r0, r1}
	bl idiv_s32
	pop {r2, r3}
	mul r1, r0, r3
	sub r12, r2, r1
	vmov s4, r12
	vcvt.f64.s32 d0, s4
	vpop {d1}
	vsub.f64 d0, d1, d0
	pop {pc}

linha_9:
	push {lr}
	ldr r0, =lit_50_0
	vldr d0, [r0]
	vpush {d0}
	ldr r0, =lit_2_0
	vldr d0, [r0]
	vpop {d1}
	vdiv.f64 d0, d1, d0
	vpush {d0}
	ldr r0, =lit_5_0
	vldr d0, [r0]
	vpush {d0}
	ldr r0, =lit_5_0
	vldr d0, [r0]
	vpop {d1}
	vmul.f64 d0, d1, d0
	vpop {d1}
	vadd.f64 d0, d1, d0
	pop {pc}

linha_10:
	push {lr}
	ldr r0, =hist
	mov r1, #72
	add r0, r0, r1
	vldr d0, [r0]
	vpush {d0}
	ldr r0, =hist
	mov r1, #64
	add r0, r0, r1
	vldr d0, [r0]
	vpop {d1}
	vadd.f64 d0, d1, d0
	pop {pc}

linha_11:
	push {lr}
	ldr r0, =lit_8_0
	vldr d0, [r0]
	vpush {d0}
	ldr r0, =lit_1_0
	vldr d0, [r0]
	vpop {d1}
	vadd.f64 d0, d1, d0
	vpush {d0}
	ldr r0, =lit_2_0
	vldr d0, [r0]
	vpush {d0}
	ldr r0, =lit_3_0
	vldr d0, [r0]
	vpop {d1}
	vmul.f64 d0, d1, d0
	vpop {d1}
	vdiv.f64 d0, d1, d0
	pop {pc}

.section .rodata
.align 3
lit_one:
	.double 1.0
lit_1_0:
	.double 1.0
lit_10_0:
	.double 10.0
lit_100_0:
	.double 100.0
lit_11_0:
	.double 11.0
lit_12_0:
	.double 12.0
lit_15_0:
	.double 15.0
lit_2_0:
	.double 2.0
lit_25_0:
	.double 25.0
lit_3_0:
	.double 3.0
lit_4_0:
	.double 4.0
lit_5_0:
	.double 5.0
lit_50_0:
	.double 50.0
lit_64_0:
	.double 64.0
lit_7_0:
	.double 7.0
lit_8_0:
	.double 8.0
lit_9_0:
	.double 9.0

.section .bss
.align 3
hist:
	.space 96
mem_BUFFER:
	.space 8

.section .bss
.align 4
stack:
	.space 65536
stack_top:

.section .text
divzero_die:
	b divzero_die
pow_neg_err:
	b pow_neg_err
