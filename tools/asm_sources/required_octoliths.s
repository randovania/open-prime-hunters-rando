// Changes the amount of Octoliths required to unlock Oubliette
// R0 holds the value for current Octoliths
// Replaces the original "and" instruction

orr     r0, r0, #0xFF       // Value to change
