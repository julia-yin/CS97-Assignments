/* Generate N bytes of random output.  */

/* When generating output this program uses the x86-64 RDRAND
   instruction if available to generate random numbers, falling back
   on /dev/random and stdio otherwise.

   This program is not portable.  Compile it with gcc -mrdrnd for a
   x86-64 machine.

   Copyright 2015, 2017, 2020 Paul Eggert

   This program is free software: you can redistribute it and/or
   modify it under the terms of the GNU General Public License as
   published by the Free Software Foundation, either version 3 of the
   License, or (at your option) any later version.

   This program is distributed in the hope that it will be useful, but
   WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

#include <errno.h>
#include <limits.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "options.h"
#include "output.h"
#include "rand64-hw.h"
#include "rand64-sw.h"
#include "mrand48_r.h"

/* Main program, which outputs N bytes of random data.  */
int
main (int argc, char **argv)
{
  /* Check arguments.  */
  long long nbytes;
  char *input = 0;
  char *output = 0;
  if (!process_options(argc, argv, &nbytes, &input, &output))
    {
      return 1;
    }

  /* If there's no work to do, don't worry about which library to use.  */
  if (nbytes == 0)
    return 0;

  /* Now that we know we have work to do, arrange to use the
     appropriate library.  */
  void (*initialize) (char *file);
  unsigned long long (*rand64) ();
  void (*finalize) (void);
  if (input == 0 || strcmp(input, "rdrand") == 0)
    {
      /* Only use hardware rand64 if default or rdrand is specified */
      if (!rdrand_supported ()) {
        fprintf(stderr, "rdrand not supported");
        return 1;
      }

      initialize = hardware_rand64_init;
      rand64 = hardware_rand64;
      finalize = hardware_rand64_fini;
    }
  else if (strcmp(input, "mrand48_r") == 0)
    {
      initialize = mrand48_rng_init;
      rand64 = mrand48_rng;
      finalize = mrand48_rng_fini;
    }
  else
    {
      /* use software if /F file is specified */
      initialize = software_rand64_init;
      rand64 = software_rand64;
      finalize = software_rand64_fini;
    }

  initialize ((input != 0 && *input == '/') ? input : "/dev/random");
  int wordsize = sizeof rand64 ();
  int output_errno = 0;

  if (output == 0 || strcmp(output, "stdio") == 0) {
    do
      {
        unsigned long long x = rand64 ();
        int outbytes = nbytes < wordsize ? nbytes : wordsize;
        if (!writebytes (x, outbytes))
	  {
	    output_errno = errno;
	    break;
	  }
        nbytes -= outbytes;
      }
    while (0 < nbytes);
  } else {
    /* Output N KiB bytes at a time, using the write system call
       Given nbytes, N
       1. malloc buffer of N * 1024 bytes
       2. For loop: repeat until nbytes == 0
         a. populate buffer with random values by using rand 64 ()
         b. write the buffer's contents to standard output (?)
         c. subtract N KiB from nbytes
    */
 
    int buffersize = atoi(output) * 1024;
    int allocate_size = 0;
    char *buf = malloc(buffersize);

    if (buf == 0) {
      fprintf(stderr, "Malloc failed, error allocating memory");
      return 1;
    }

    do
      {
        /* allocate_size is the minimum between N*1024 and nbytes */
        allocate_size = (nbytes > buffersize) ? buffersize : nbytes;
        int num_64bits = allocate_size / 8;
        int i = 0;

        /* Generate random 64 bits and place into buffer */
        for (; i < num_64bits; i++)
          write_bytes(&buf[i*8], 8, rand64());

        /* Check for remainders: nbytes not a multiple of 8 */
        if (allocate_size == nbytes) {
          int remainder = allocate_size % 8;
          if (remainder != 0)
            write_bytes(&buf[i*8], remainder, rand64());
        }

        /* Write the buffer to standard output */
        write(1, buf, allocate_size);
        nbytes -= allocate_size;
      }
    while (0 < nbytes);
    
    free(buf);
  }

  if (fclose (stdout) != 0)
    output_errno = errno;

  if (output_errno)
    {
      errno = output_errno;
      perror ("output");
    }

  finalize ();
  return !!output_errno;
}
