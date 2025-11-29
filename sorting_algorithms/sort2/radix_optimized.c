#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// ==============================================================
// BYTE-OPTIMIZED RADIX SORT
//
// Key optimizations:
// 1. 8-bit digits (k=256) - count array fits in L1 cache
// 2. Bit shifts instead of division/modulo
// 3. Single-pass histogram: build ALL byte histograms in one pass
// 4. Ping-pong buffers (no redundant memcpy)
// 5. Skip pass if all values have same byte (already sorted for that digit)
// ==============================================================

#define RADIX_BITS 8
#define RADIX_SIZE (1 << RADIX_BITS) // 256
#define RADIX_MASK (RADIX_SIZE - 1)  // 0xFF

// Extract byte at position (0 = LSB, 3 = MSB for 32-bit)
#define GET_BYTE(val, byte_pos)                                                \
  (((val) >> ((byte_pos) * RADIX_BITS)) & RADIX_MASK)

// Number of bytes in uint32_t
#define NUM_PASSES 4

void radix_sort_u32(uint32_t *A, size_t n) {
  if (n <= 1)
    return;

  uint32_t *B = (uint32_t *)malloc(n * sizeof(uint32_t));
  if (!B)
    return;

  // Histograms for all 4 byte positions (computed in single pass)
  size_t hist[NUM_PASSES][RADIX_SIZE] = {0};

  // === PHASE 1: Build all histograms in ONE pass through data ===
  for (size_t i = 0; i < n; i++) {
    uint32_t val = A[i];
    hist[0][GET_BYTE(val, 0)]++;
    hist[1][GET_BYTE(val, 1)]++;
    hist[2][GET_BYTE(val, 2)]++;
    hist[3][GET_BYTE(val, 3)]++;
  }

  // === PHASE 2: Distribution passes ===
  uint32_t *src = A;
  uint32_t *dst = B;

  for (int pass = 0; pass < NUM_PASSES; pass++) {
    size_t *count = hist[pass];

    // Check if this pass can be skipped (all values have same byte)
    // This happens when one bucket has all n elements
    bool skip = false;
    for (int i = 0; i < RADIX_SIZE; i++) {
      if (count[i] == n) {
        skip = true;
        break;
      }
    }

    if (skip)
      continue; // All elements have same byte at this position

    // Convert counts to cumulative offsets (prefix sum)
    size_t total = 0;
    for (int i = 0; i < RADIX_SIZE; i++) {
      size_t c = count[i];
      count[i] = total;
      total += c;
    }

    // Distribute elements to destination
    for (size_t i = 0; i < n; i++) {
      uint32_t val = src[i];
      size_t byte_val = GET_BYTE(val, pass);
      dst[count[byte_val]++] = val;
    }

    // Swap src and dst for next pass
    uint32_t *tmp = src;
    src = dst;
    dst = tmp;
  }

  // If result ended up in B, copy back to A
  if (src != A) {
    memcpy(A, src, n * sizeof(uint32_t));
  }

  free(B);
}

// ==============================================================
// STANDARD RADIX SORT (for comparison)
// ==============================================================
void radix_sort_standard(uint32_t *A, size_t n, int d, int k) {
  uint32_t *B = (uint32_t *)malloc(n * sizeof(uint32_t));
  size_t *C = (size_t *)calloc(k, sizeof(size_t));

  uint32_t *src = A;
  uint32_t *dst = B;

  uint32_t divisor = 1;
  for (int digit = 0; digit < d; digit++) {
    memset(C, 0, k * sizeof(size_t));

    // Count
    for (size_t i = 0; i < n; i++) {
      C[(src[i] / divisor) % k]++;
    }

    // Prefix sum
    for (int i = 1; i < k; i++) {
      C[i] += C[i - 1];
    }

    // Distribute (backwards for stability)
    for (size_t i = n; i > 0; i--) {
      uint32_t val = src[i - 1];
      size_t idx = (val / divisor) % k;
      dst[--C[idx]] = val;
    }

    uint32_t *tmp = src;
    src = dst;
    dst = tmp;
    divisor *= k;
  }

  if (src != A) {
    memcpy(A, src, n * sizeof(uint32_t));
  }

  free(B);
  free(C);
}

// ==============================================================
// QUICKSORT (for comparison)
// ==============================================================
int cmp_u32(const void *a, const void *b) {
  uint32_t ua = *(const uint32_t *)a;
  uint32_t ub = *(const uint32_t *)b;
  return (ua > ub) - (ua < ub);
}

void quicksort_stdlib(uint32_t *A, size_t n) {
  qsort(A, n, sizeof(uint32_t), cmp_u32);
}

// ==============================================================
// UTILITIES
// ==============================================================
bool is_sorted(uint32_t *A, size_t n) {
  for (size_t i = 0; i < n - 1; i++) {
    if (A[i] > A[i + 1])
      return false;
  }
  return true;
}

void fill_random(uint32_t *A, size_t n) {
  for (size_t i = 0; i < n; i++) {
    // Full 32-bit range
    A[i] = ((uint32_t)rand() << 16) ^ (uint32_t)rand();
  }
}

uint32_t *copy_array(uint32_t *A, size_t n) {
  uint32_t *B = (uint32_t *)malloc(n * sizeof(uint32_t));
  memcpy(B, A, n * sizeof(uint32_t));
  return B;
}

double time_ms(clock_t start, clock_t end) {
  return ((double)(end - start)) / CLOCKS_PER_SEC * 1000.0;
}

// ==============================================================
// BENCHMARK
// ==============================================================
#define WARMUP 2
#define RUNS 5

double median(double *arr, int n) {
  // Simple bubble sort for tiny array
  for (int i = 0; i < n - 1; i++) {
    for (int j = 0; j < n - i - 1; j++) {
      if (arr[j] > arr[j + 1]) {
        double tmp = arr[j];
        arr[j] = arr[j + 1];
        arr[j + 1] = tmp;
      }
    }
  }
  return arr[n / 2];
}

typedef struct {
  double optimized_ms;
  double standard_ms;
  double qsort_ms;
} Result;

Result benchmark(size_t n) {
  Result r = {0};
  uint32_t *original = (uint32_t *)malloc(n * sizeof(uint32_t));
  fill_random(original, n);

  clock_t start, end;
  double times[RUNS];

  // Byte-optimized radix
  for (int w = 0; w < WARMUP; w++) {
    uint32_t *arr = copy_array(original, n);
    radix_sort_u32(arr, n);
    free(arr);
  }
  for (int i = 0; i < RUNS; i++) {
    uint32_t *arr = copy_array(original, n);
    start = clock();
    radix_sort_u32(arr, n);
    end = clock();
    times[i] = time_ms(start, end);
    if (!is_sorted(arr, n))
      printf("ERROR: optimized not sorted!\n");
    free(arr);
  }
  r.optimized_ms = median(times, RUNS);

  // Standard radix (base 10, 10 digits for full 32-bit range)
  for (int w = 0; w < WARMUP; w++) {
    uint32_t *arr = copy_array(original, n);
    radix_sort_standard(arr, n, 10, 10); // 10 decimal digits
    free(arr);
  }
  for (int i = 0; i < RUNS; i++) {
    uint32_t *arr = copy_array(original, n);
    start = clock();
    radix_sort_standard(arr, n, 10, 10);
    end = clock();
    times[i] = time_ms(start, end);
    if (!is_sorted(arr, n))
      printf("ERROR: standard not sorted!\n");
    free(arr);
  }
  r.standard_ms = median(times, RUNS);

  // stdlib qsort
  for (int w = 0; w < WARMUP; w++) {
    uint32_t *arr = copy_array(original, n);
    quicksort_stdlib(arr, n);
    free(arr);
  }
  for (int i = 0; i < RUNS; i++) {
    uint32_t *arr = copy_array(original, n);
    start = clock();
    quicksort_stdlib(arr, n);
    end = clock();
    times[i] = time_ms(start, end);
    free(arr);
  }
  r.qsort_ms = median(times, RUNS);

  free(original);
  return r;
}

// ==============================================================
// MAIN
// ==============================================================
// clang-format off
int main() {
    srand(42);

    printf("\n");
    printf("┌───────────────────────────────────────────────────────────────────────┐\n");
    printf("│              BYTE-OPTIMIZED RADIX SORT BENCHMARK                      │\n");
    printf("│              Full 32-bit unsigned integers (0 to 2^32-1)              │\n");
    printf("│              Median of %d runs, %d warmup                               │\n", RUNS, WARMUP);
    printf("├─────────────┬──────────────────┬──────────────────┬────────────────────┤\n");
    printf("│  Array Size │ Radix (8-bit)    │ Radix (base 10)  │   stdlib qsort     │\n");
    printf("│             │ 4 passes, k=256  │ 10 passes, k=10  │   O(n log n)       │\n");
    printf("├─────────────┼──────────────────┼──────────────────┼────────────────────┤\n");

    size_t sizes[] = {10000, 100000, 1000000, 5000000, 10000000};
    int num_sizes = sizeof(sizes) / sizeof(sizes[0]);

    for (int i = 0; i < num_sizes; i++) {
        Result r = benchmark(sizes[i]);
        printf("│ %10zu  │ %12.2f ms  │ %12.2f ms  │ %12.2f ms    │\n",
               sizes[i], r.optimized_ms, r.standard_ms, r.qsort_ms);
    }

    printf("└─────────────┴──────────────────┴──────────────────┴────────────────────┘\n");

    printf("\n");
    printf("Why byte-optimized is faster:\n");
    printf("  • 4 passes vs 10 passes (fewer cache misses)\n");
    printf("  • Bit shifts vs division/modulo (much faster)\n");
    printf("  • Single-pass histogram (reads data once, not 4 times)\n");
    printf("  • k=256 count array fits in L1 cache (1KB)\n");
    printf("  • Skip optimization: skips passes where all bytes are equal\n");
    printf("\n");
    printf("Memory usage:\n");
    printf("  • Radix (8-bit):   O(n) + 4×256 = O(n) + 1KB\n");
    printf("  • Radix (base 10): O(n) + 10 words\n");
    printf("  • qsort:           O(log n) stack\n");
    printf("\n");

    return 0;
}
// clang-format on
