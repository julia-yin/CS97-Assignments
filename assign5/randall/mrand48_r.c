#include <stdio.h>
#include <stdlib.h>

#include "mrand48_r.h"

struct drand48_data buf = {0};

/* Initialize the mrand48_r random function */
void 
mrand48_rng_init(char *file)
{
  long int seed = time(NULL);
  srand48_r(seed, &buf);
}

/* Generate random numbers using mrand48_r */
unsigned long long
mrand48_rng()
{
  long int a, b;
  mrand48_r(&buf, &a);
  mrand48_r(&buf, &b); // using the same buf!
  return ((((unsigned long long) a) << 32) |
          ((unsigned long long) b & 0x00000000FFFFFFFF));
}

/* Finalize the mrand48_r function */
void
mrand48_rng_fini()
{
}
