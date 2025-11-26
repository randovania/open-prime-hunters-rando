/*
Register values at the start of the snippet
R0: 17 (id value of Cloak)
R4: Bool value of 1 (part of processing)
R6: #0
*/

ldr     r0, [r8,#0x4C8]   // processed = 1
mov     r6, r4
ldr     r0, [sp,#0x38]  // state
mov     r1, #0x38       // string message id
ldr     lr, =0x0201A3DC // load the address of UA Expansion show dialog (same function for all single player items)
bx      lr