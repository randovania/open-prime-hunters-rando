// The following instructions have been reordered to support changing the value of R0 for starting Octoliths
strb r0, [r4, 24h]
strb r0, [r4, 26h]
mov r0, #0
mov r1, r0
mov r2, r0
mov r3, r0
strh sb, [r4, #0xa]
strh r8, [r4, #0xc]
strh r7, [r4, #0xe]
