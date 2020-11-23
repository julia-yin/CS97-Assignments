#include <errno.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>

#include "options.h"

bool
process_options(int argc, char **argv, long long *nbytes, char **input, char **output)
{
  if (argc < 2)
    return false;

  int c;
  int errflg = 0;

  while ((c = getopt(argc, argv, "i:o:")) != -1) {
    switch(c) {
      case 'i':
          *input = optarg;
          if (strcmp(*input, "rdrand") != 0 &&
              strcmp(*input, "mrand48_r") != 0 &&
              **input != '/') {
              fprintf(stderr,
                  "Option -i invalid operand\n");
              return false;
          }
          break;
      case 'o':
          *output = optarg;
          break;
      case ':':       /* -i or -o without operand */
          fprintf(stderr,
              "Option -%c requires an operand\n", optopt);
          errflg++;
          return false;
          break;
      case '?':
          fprintf(stderr,
              "Unrecognized option: '-%c'\n", optopt);
          errflg++;
          return false;
    }
  }

  if (optind < (argc - 1)) {
    fprintf(stderr, "Invalid number of operands\n%s: usage: %s NBYTES [options]\n", argv[0], argv[0]);
    return false;
  }

  char *endptr;
  *nbytes = strtoll (argv[optind == argc ? 1 : optind], &endptr, 10);

  if (*nbytes < 0 || *endptr) {
    fprintf(stderr, "Number of bytes invalid: must be a positive integer");
    return 1;
  }

  errno = 0;
  if (errno) {
    perror (argv[optind == argc ? 1 : optind]);
    return false;
  }

  return true;
}
