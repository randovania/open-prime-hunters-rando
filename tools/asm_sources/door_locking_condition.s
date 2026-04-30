// Replaces the 2nd conditional of the door locking if statement to check the custom random encounters flag instead of the player count

@ADDRESS: 0x02053B3C
ldrb    r0, [r0,#0xD]       // Load the custom spawn flag
cmp     r0, #1              // Compare to 1
bne     0x02053BB8          // Branch into the locking code if not equal
