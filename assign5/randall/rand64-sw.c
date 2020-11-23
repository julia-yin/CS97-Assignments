#include <string.h>
#include "rand64-sw.h"

/* Software implementation.  */

/* Input stream containing random bytes.  */
FILE *urandstream;

/* Initialize the software rand64 implementation.  */
void
software_rand64_init (char *file)
{
  if (file == 0)
    abort ();
  urandstream = fopen (file, "r");
  if (! urandstream)
    abort ();
}

/* Return a random value, using software operations.  */
unsigned long long
software_rand64 ()
{
  unsigned long long int x;
  if (fread (&x, sizeof x, 1, urandstream) != 1)
    abort ();
  return x;
}

/* Finalize the software rand64 implementation.  */
void
software_rand64_fini (void)
{
  fclose (urandstream);
}

