#ifndef MRAND48R_H
#define MRAND48R_H

/* Initialize the mrand48_r random function */
void
mrand48_rng_init(char *file);

/* Generate random numbers using mrand48_r */
unsigned long long
mrand48_rng();

/* Finalize the mrand48_r function */
void
mrand48_rng_fini();

#endif
