#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// ==============================================================
// RADIX SORT WITH CONFIGURABLE BIT WIDTH
//
// Trade-off: fewer bits = smaller buckets but more passes
//   4-bit:  k=16,    d=8 passes (tiny buckets, many passes)
//   8-bit:  k=256,   d=4 passes (sweet spot for most CPUs)
//   11-bit: k=2048,  d=3 passes (fewer passes, larger buckets)
//   16-bit: k=65536, d=2 passes (huge buckets, cache pressure)
// ==============================================================

// Extract bits [bit_pos, bit_pos + width) from val
#define GET_BITS(val, bit_pos, mask) (((val) >> (bit_pos)) & (mask))

// ==============================================================
// 4-BIT RADIX (NIBBLE) - k=16, 8 passes
// ==============================================================
#define RADIX_4_SIZE 16
#define RADIX_4_MASK 0xF
#define RADIX_4_PASSES 8

void radix_sort_4bit(uint32_t *A, size_t n) {
  if (n <= 1)
    return;

  uint32_t *B = malloc(n * sizeof(uint32_t));
  if (!B)
    return;

  // Build all 8 histograms in single pass
  size_t hist[RADIX_4_PASSES][RADIX_4_SIZE] = {0};

  for (size_t i = 0; i < n; i++) {
    uint32_t val = A[i];
    hist[0][GET_BITS(val, 0, RADIX_4_MASK)]++;
    hist[1][GET_BITS(val, 4, RADIX_4_MASK)]++;
    hist[2][GET_BITS(val, 8, RADIX_4_MASK)]++;
    hist[3][GET_BITS(val, 12, RADIX_4_MASK)]++;
    hist[4][GET_BITS(val, 16, RADIX_4_MASK)]++;
    hist[5][GET_BITS(val, 20, RADIX_4_MASK)]++;
    hist[6][GET_BITS(val, 24, RADIX_4_MASK)]++;
    hist[7][GET_BITS(val, 28, RADIX_4_MASK)]++;
  }

  uint32_t *src = A;
  uint32_t *dst = B;

  for (int pass = 0; pass < RADIX_4_PASSES; pass++) {
    int bit_pos = pass * 4;
    size_t *count = hist[pass];

    // Skip if all elements have same nibble
    bool skip = false;
    for (int i = 0; i < RADIX_4_SIZE; i++) {
      if (count[i] == n) {
        skip = true;
        break;
      }
    }
    if (skip)
      continue;

    // Prefix sum
    size_t total = 0;
    for (int i = 0; i < RADIX_4_SIZE; i++) {
      size_t c = count[i];
      count[i] = total;
      total += c;
    }

    // Distribute
    for (size_t i = 0; i < n; i++) {
      uint32_t val = src[i];
      size_t idx = GET_BITS(val, bit_pos, RADIX_4_MASK);
      dst[count[idx]++] = val;
    }

    uint32_t *tmp = src;
    src = dst;
    dst = tmp;
  }

  if (src != A)
    memcpy(A, src, n * sizeof(uint32_t));
  free(B);
}

// ==============================================================
// 8-BIT RADIX (BYTE) - k=256, 4 passes
// ==============================================================
#define RADIX_8_SIZE 256
#define RADIX_8_MASK 0xFF
#define RADIX_8_PASSES 4

void radix_sort_8bit(uint32_t *A, size_t n) {
  if (n <= 1)
    return;

  uint32_t *B = malloc(n * sizeof(uint32_t));
  if (!B)
    return;

  size_t hist[RADIX_8_PASSES][RADIX_8_SIZE] = {0};

  for (size_t i = 0; i < n; i++) {
    uint32_t val = A[i];
    hist[0][GET_BITS(val, 0, RADIX_8_MASK)]++;
    hist[1][GET_BITS(val, 8, RADIX_8_MASK)]++;
    hist[2][GET_BITS(val, 16, RADIX_8_MASK)]++;
    hist[3][GET_BITS(val, 24, RADIX_8_MASK)]++;
  }

  uint32_t *src = A;
  uint32_t *dst = B;

  for (int pass = 0; pass < RADIX_8_PASSES; pass++) {
    int bit_pos = pass * 8;
    size_t *count = hist[pass];

    bool skip = false;
    for (int i = 0; i < RADIX_8_SIZE; i++) {
      if (count[i] == n) {
        skip = true;
        break;
      }
    }
    if (skip)
      continue;

    size_t total = 0;
    for (int i = 0; i < RADIX_8_SIZE; i++) {
      size_t c = count[i];
      count[i] = total;
      total += c;
    }

    for (size_t i = 0; i < n; i++) {
      uint32_t val = src[i];
      size_t idx = GET_BITS(val, bit_pos, RADIX_8_MASK);
      dst[count[idx]++] = val;
    }

    uint32_t *tmp = src;
    src = dst;
    dst = tmp;
  }

  if (src != A)
    memcpy(A, src, n * sizeof(uint32_t));
  free(B);
}

// ==============================================================
// 11-BIT RADIX - k=2048, 3 passes (32 bits / 11 ≈ 3)
// ==============================================================
#define RADIX_11_SIZE 2048
#define RADIX_11_MASK 0x7FF

void radix_sort_11bit(uint32_t *A, size_t n) {
  if (n <= 1)
    return;

  uint32_t *B = malloc(n * sizeof(uint32_t));
  if (!B)
    return;

  // 3 passes: bits 0-10, 11-21, 22-31 (last one is 10 bits)
  size_t hist[3][RADIX_11_SIZE] = {0};

  for (size_t i = 0; i < n; i++) {
    uint32_t val = A[i];
    hist[0][GET_BITS(val, 0, RADIX_11_MASK)]++;
    hist[1][GET_BITS(val, 11, RADIX_11_MASK)]++;
    hist[2][GET_BITS(val, 22, 0x3FF)]++; // Only 10 bits left
  }

  uint32_t *src = A;
  uint32_t *dst = B;

  int bit_positions[] = {0, 11, 22};
  int masks[] = {RADIX_11_MASK, RADIX_11_MASK, 0x3FF};
  int sizes[] = {RADIX_11_SIZE, RADIX_11_SIZE, 1024};

  for (int pass = 0; pass < 3; pass++) {
    int bit_pos = bit_positions[pass];
    int mask = masks[pass];
    int k = sizes[pass];
    size_t *count = hist[pass];

    bool skip = false;
    for (int i = 0; i < k; i++) {
      if (count[i] == n) {
        skip = true;
        break;
      }
    }
    if (skip)
      continue;

    size_t total = 0;
    for (int i = 0; i < k; i++) {
      size_t c = count[i];
      count[i] = total;
      total += c;
    }

    for (size_t i = 0; i < n; i++) {
      uint32_t val = src[i];
      size_t idx = GET_BITS(val, bit_pos, mask);
      dst[count[idx]++] = val;
    }

    uint32_t *tmp = src;
    src = dst;
    dst = tmp;
  }

  if (src != A)
    memcpy(A, src, n * sizeof(uint32_t));
  free(B);
}

// ==============================================================
// 16-BIT RADIX - k=65536, 2 passes
// ==============================================================
#define RADIX_16_SIZE 65536
#define RADIX_16_MASK 0xFFFF

void radix_sort_16bit(uint32_t *A, size_t n) {
  if (n <= 1)
    return;

  uint32_t *B = malloc(n * sizeof(uint32_t));
  if (!B)
    return;

  size_t *hist0 = calloc(RADIX_16_SIZE, sizeof(size_t));
  size_t *hist1 = calloc(RADIX_16_SIZE, sizeof(size_t));

  for (size_t i = 0; i < n; i++) {
    uint32_t val = A[i];
    hist0[GET_BITS(val, 0, RADIX_16_MASK)]++;
    hist1[GET_BITS(val, 16, RADIX_16_MASK)]++;
  }

  uint32_t *src = A;
  uint32_t *dst = B;

  // Pass 0: low 16 bits
  {
    size_t total = 0;
    for (int i = 0; i < RADIX_16_SIZE; i++) {
      size_t c = hist0[i];
      hist0[i] = total;
      total += c;
    }
    for (size_t i = 0; i < n; i++) {
      uint32_t val = src[i];
      size_t idx = GET_BITS(val, 0, RADIX_16_MASK);
      dst[hist0[idx]++] = val;
    }
    uint32_t *tmp = src;
    src = dst;
    dst = tmp;
  }

  // Pass 1: high 16 bits
  {
    size_t total = 0;
    for (int i = 0; i < RADIX_16_SIZE; i++) {
      size_t c = hist1[i];
      hist1[i] = total;
      total += c;
    }
    for (size_t i = 0; i < n; i++) {
      uint32_t val = src[i];
      size_t idx = GET_BITS(val, 16, RADIX_16_MASK);
      dst[hist1[idx]++] = val;
    }
    uint32_t *tmp = src;
    src = dst;
    dst = tmp;
  }

  if (src != A)
    memcpy(A, src, n * sizeof(uint32_t));
  free(hist0);
  free(hist1);
  free(B);
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
    A[i] = ((uint32_t)rand() << 16) ^ (uint32_t)rand();
  }
}

uint32_t *copy_array(uint32_t *A, size_t n) {
  uint32_t *B = malloc(n * sizeof(uint32_t));
  memcpy(B, A, n * sizeof(uint32_t));
  return B;
}

double time_ms(clock_t start, clock_t end) {
  return ((double)(end - start)) / CLOCKS_PER_SEC * 1000.0;
}

double median(double *arr, int n) {
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

// ==============================================================
// BENCHMARK
// ==============================================================
#define WARMUP 2
#define RUNS 5

typedef struct {
  double t4, t8, t11, t16;
} Result;

Result benchmark(size_t n) {
  Result r = {0};
  uint32_t *original = malloc(n * sizeof(uint32_t));
  fill_random(original, n);

  clock_t start, end;
  double times[RUNS];

  // 4-bit
  for (int w = 0; w < WARMUP; w++) {
    uint32_t *arr = copy_array(original, n);
    radix_sort_4bit(arr, n);
    free(arr);
  }
  for (int i = 0; i < RUNS; i++) {
    uint32_t *arr = copy_array(original, n);
    start = clock();
    radix_sort_4bit(arr, n);
    end = clock();
    times[i] = time_ms(start, end);
    if (!is_sorted(arr, n))
      printf("4-bit FAILED!\n");
    free(arr);
  }
  r.t4 = median(times, RUNS);

  // 8-bit
  for (int w = 0; w < WARMUP; w++) {
    uint32_t *arr = copy_array(original, n);
    radix_sort_8bit(arr, n);
    free(arr);
  }
  for (int i = 0; i < RUNS; i++) {
    uint32_t *arr = copy_array(original, n);
    start = clock();
    radix_sort_8bit(arr, n);
    end = clock();
    times[i] = time_ms(start, end);
    if (!is_sorted(arr, n))
      printf("8-bit FAILED!\n");
    free(arr);
  }
  r.t8 = median(times, RUNS);

  // 11-bit
  for (int w = 0; w < WARMUP; w++) {
    uint32_t *arr = copy_array(original, n);
    radix_sort_11bit(arr, n);
    free(arr);
  }
  for (int i = 0; i < RUNS; i++) {
    uint32_t *arr = copy_array(original, n);
    start = clock();
    radix_sort_11bit(arr, n);
    end = clock();
    times[i] = time_ms(start, end);
    if (!is_sorted(arr, n))
      printf("11-bit FAILED!\n");
    free(arr);
  }
  r.t11 = median(times, RUNS);

  // 16-bit
  for (int w = 0; w < WARMUP; w++) {
    uint32_t *arr = copy_array(original, n);
    radix_sort_16bit(arr, n);
    free(arr);
  }
  for (int i = 0; i < RUNS; i++) {
    uint32_t *arr = copy_array(original, n);
    start = clock();
    radix_sort_16bit(arr, n);
    end = clock();
    times[i] = time_ms(start, end);
    if (!is_sorted(arr, n))
      printf("16-bit FAILED!\n");
    free(arr);
  }
  r.t16 = median(times, RUNS);

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
    printf("┌──────────────────────────────────────────────────────────────────────────────────┐\n");
    printf("│                    RADIX SORT: BIT WIDTH COMPARISON                              │\n");
    printf("│                    Full 32-bit unsigned integers                                 │\n");
    printf("├──────────────┬──────────────┬──────────────┬──────────────┬───────────────────────┤\n");
    printf("│  Array Size  │  4-bit       │  8-bit       │  11-bit      │  16-bit               │\n");
    printf("│              │  k=16, d=8   │  k=256, d=4  │  k=2048, d=3 │  k=65536, d=2         │\n");
    printf("├──────────────┼──────────────┼──────────────┼──────────────┼───────────────────────┤\n");

    size_t sizes[] = {10000, 100000, 1000000, 5000000, 10000000};
    int num_sizes = sizeof(sizes) / sizeof(sizes[0]);

    for (int i = 0; i < num_sizes; i++) {
        Result r = benchmark(sizes[i]);
        printf("│ %11zu  │ %8.2f ms  │ %8.2f ms  │ %8.2f ms  │ %10.2f ms         │\n",
               sizes[i], r.t4, r.t8, r.t11, r.t16);
    }

    printf("└──────────────┴──────────────┴──────────────┴──────────────┴───────────────────────┘\n");

    printf("\n");
    printf("┌──────────────────────────────────────────────────────────────────────────────────┐\n");
    printf("│                           TRADE-OFF ANALYSIS                                     │\n");
    printf("├──────────┬────────┬────────┬───────────────────────────────────────────────────────┤\n");
    printf("│ Bit Width│ Buckets│ Passes │ Count Array Size                                    │\n");
    printf("├──────────┼────────┼────────┼───────────────────────────────────────────────────────┤\n");
    printf("│  4-bit   │   16   │   8    │ 16 × 8 bytes = 128 bytes (fits in registers!)       │\n");
    printf("│  8-bit   │  256   │   4    │ 256 × 8 bytes = 2 KB (fits in L1 cache)             │\n");
    printf("│ 11-bit   │ 2048   │   3    │ 2048 × 8 bytes = 16 KB (fits in L1 cache)           │\n");
    printf("│ 16-bit   │ 65536  │   2    │ 65536 × 8 bytes = 512 KB (L2/L3 cache)              │\n");
    printf("└──────────┴────────┴────────┴───────────────────────────────────────────────────────┘\n");

    printf("\n");
    printf("Key insights:\n");
    printf("  • 4-bit: Tiny buckets but 8 passes = too many data scans\n");
    printf("  • 8-bit: Sweet spot - L1 cache friendly, reasonable passes\n");
    printf("  • 11-bit: Fewer passes, still L1 cache friendly\n");
    printf("  • 16-bit: Only 2 passes but 512KB count array = cache thrashing\n");
    printf("\n");
    printf("Low-level details:\n");
    printf("  • GET_BITS(val, pos, mask) = (val >> pos) & mask\n");
    printf("  • 4-bit mask: 0xF,  8-bit: 0xFF,  16-bit: 0xFFFF\n");
    printf("  • All use single-pass histogram for all digits\n");
    printf("  • All use ping-pong buffers (no redundant memcpy)\n");
    printf("\n");

    return 0;
}
// clang-format on
