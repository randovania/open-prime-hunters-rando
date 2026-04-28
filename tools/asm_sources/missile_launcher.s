/*
Register values at the start of the snippet
R0: 21 (id value of Affinity Weapon)
R1: #0
R2: value of the ammo cap
R8: ???
R12: more ammo caps?
*/

// ammo caps
add     r12, r8, #0x100
ldrh    r2, [r12,#0x52]
ldr     r0, [sp,#0x38]  // state
add     r2, r2, #0x32   // ammo given when picked up
mov     r1, #0x37       // string message id
ldr     lr, =0x0201A354 // load the address of the story save ammo update in missile expansions function
bx      lr
