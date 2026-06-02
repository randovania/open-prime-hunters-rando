// Overwrites the original `hud_up_cloak_base` case with custom code to load Missile Launcher instructions

@ADDRESS: 0x0202D594
mov     r0, #0x64           // The custom string ID
bl      0x0203C2E0          // get_hud_string address
str     r0, [sp, #0x20]     // Write the pointer
b       0x0202DAC0          // Branch back to the Weapon Unlocked switch case
