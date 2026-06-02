// Adds a custom Missile Launcher item which is required in order to fire Missiles

@ADDRESS: 0x02019E80
nop                         // Nop out the hunter check for Samus
nop
add     r0, r8, #0x100      // r8 holds the CPlayer struct
ldrh    r1, [r0, #0x52]     // Load the player offset for ammo
add     r1, r1, #0x32       // Ammo given on pickup  
strh    r1, [r0, #0x52]     // Store the value in the CPlayer
ldrh    lr, [r0, #0x52]     // Ammo recovery block
ldrh    r9, [r0, #0x4E]
sub     r9, lr, r9
strh    r9, [r0, #0x56]
ldrh    r11, [r0, #0x52]
ldr     r0, =0x020E9710     // Load story_save into r0
strh    r11, [r0, #0xC]     // Store the new ammo_cap value
mov     r9, #2              // Set the weapon_id to 2 (unlocks missiles)
b       0x02019ED8          // Branch to update_hud
nop                         // Nop out the rest of the unused affinity weapon code
nop
nop
nop
nop
nop
