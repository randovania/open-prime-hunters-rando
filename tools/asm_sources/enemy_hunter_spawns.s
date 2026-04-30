// Sets the random spawn encounter flag to 1

mov     r1, #1              // Set the flag value to 1
strb    r1, [r4,#0xD]       // Load the new value into the flag address
nop                         // Nop out the cmp
