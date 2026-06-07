// Overwrites the original conditional regarding game_state
// Sets how much ammo is recovered from an ammo refill


add     r0, r8, r9, lsl#1   // self->ammo[slot] + ammo refill
add     r0, r0, #0x100
ldrh    r1, [r0, #0x4C]
ldr     r2, [pc, #8]        // load the placeholder value
add     r1, r1, r2          // add the value
strh    r1, [r0, #0x4C]
b       #0x1C               // branch to play_sfx
.word   0xFF                // placeholder value for ammo
nop                         // nop out unused code from the conditional
nop
nop
nop
nop
nop
