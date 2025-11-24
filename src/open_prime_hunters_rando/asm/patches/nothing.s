ldr     r0, [r8,#0x4C8]   // processed = 1
mov     r6, r4
ldr     r0, [sp,#0x38]  // state
mov     r1, #0x38       // string message id
ldr     lr, =0x0201A3DC // load the address of UA Expansion show dialog (same for all standard items)
bx      lr