#ifndef RAND64SW_H
#define RAND64SW_H

#include <stdio.h>
#include <stdlib.h>

/* Initialize the software rand64 implementation.  */
void
software_rand64_init (char *file);

/* Return a random value, using software operations.  */
unsigned long long
software_rand64 ();

/* Finalize the software rand64 implementation.  */
void
software_rand64_fini (void);

#endif
