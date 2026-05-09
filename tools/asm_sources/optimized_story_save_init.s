// This optimizes a large portion of the original code to free up space to handle starting with Artifacts.
// This also handles which planets are unlocked since that change happens in this block, so it's all been combined.

mov     r9, #0x7B               // r9 takes the place of r4
loop_wipe:
    stm     r5!, {r0-r3}
    stm     r5!, {r0-r3}
    subs    r9, r9, #1          // r9 takes the place of r4
    bne     loop_wipe
stm     r5!, {r0-r3}
stm     r5, {r0, r1}
mov     r0, #0
mov     r1, r0
mov     r3, r0
mov     r9, r0
add     r2, r4, #0xF00          // story_save is loaded in r4
add     r2, r2, #0xCC           // #0xFCC: enemy_encounters in story_save
stm     r2!, {r0, r1, r3, r9}
stm     r2!, {r0, r1, r3, r9}
stm     r2!, {r0, r1, r3, r9}
stm     r2!, {r0, r1, r3, r9}
stm     r2, {r0, r1}
add     r2, r2, #0x50           // #0x101C: logbook in story_save
stm     r2!, {r0, r1, r3, r9}
stm     r2!, {r0, r1, r3, r9}
stm     r2!, {r0, r1, r3, r9}
stm     r2!, {r0, r1, r3, r9}
stm     r2!, {r0, r1, r3, r9}
stm     r2!, {r0, r1, r3, r9}
ldr     r0, =0xFFFFFFFF         // Artifact mask
str     r0, [r4, #0x1C]
mov     r1, #0xC                // Unlocked planets
strh    r1, [r4, #0x12]
str     r3, [r4, #0x18]
mov     r9, #1
sub     r2, r2, #0x1C           // #0x1000: field_1000 in story_save
mov     r5, r9
add     r7, r4, r9, LSR#3
nop
nop
