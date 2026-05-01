// Replaces the first condition of the `init_enemy_hunter_spawns()` function with a custom flag to detect if random spawns have been activated

mov     r1, #0             // Set the flag value to 0
strb    r1, [r2,#0xD]      // Load the new value into the flag address
nop                        // NOP out the final instructions of the original condition
nop
nop
