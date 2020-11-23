#ifndef RAND64HW_H
#define RAND64HW_H

#include <cpuid.h>
#include <immintrin.h>

/* Description of the current CPU.  */
struct cpuid { unsigned eax, ebx, ecx, edx; };

/* Return information about the CPU.  See <http://wiki.osdev.org/CPUID>.  */
struct cpuid
cpuid (unsigned int leaf, unsigned int subleaf);

/* Return true if the CPU supports the RDRAND instruction.  */
_Bool
rdrand_supported (void);

/* Initialize the hardware rand64 implementation.  */
void
hardware_rand64_init (char *file);

/* Return a random value, using hardware operations.  */
unsigned long long
hardware_rand64 ();

/* Finalize the hardware rand64 implementation.  */
void
hardware_rand64_fini (void);

#endif
