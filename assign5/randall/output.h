#ifndef OUTPUT_H
#define OUTPUT_H

#include <stdbool.h>

bool writebytes (unsigned long long x, int nbytes);
static inline void write_bytes (char *buf, int bytes, unsigned long long x)
{
  for (int j = 0; j < bytes; j++)
    buf[j] = *((unsigned char *)&x + j);
}
#endif
