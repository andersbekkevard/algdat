#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// ==============================================================
// INSERTION SORT - O(n²)
// ==============================================================
void insertion_sort(int *A, int n) {
  for (int i = 1; i < n; i++) {
    int key = A[i];
    int j = i - 1;
    while (j >= 0 && A[j] > key) {
      A[j + 1] = A[j];
      j--;
    }
    A[j + 1] = key;
  }
}

// ==============================================================
// QUICKSORT - O(n log n) average, O(n²) worst
// Inlined swap for fair comparison
// ==============================================================
int partition(int *A, int lo, int hi) {
  int pivot = A[hi];
  int i = lo - 1;
  for (int j = lo; j < hi; j++) {
    if (A[j] <= pivot) {
      i++;
      int tmp = A[i];
      A[i] = A[j];
      A[j] = tmp;
    }
  }
  int tmp = A[i + 1];
  A[i + 1] = A[hi];
  A[hi] = tmp;
  return i + 1;
}

void quicksort_helper(int *A, int lo, int hi) {
  if (lo < hi) {
    int p = partition(A, lo, hi);
    quicksort_helper(A, lo, p - 1);
    quicksort_helper(A, p + 1, hi);
  }
}

void quicksort(int *A, int n) { quicksort_helper(A, 0, n - 1); }

// ==============================================================
// RADIX SORT (LSD) - O(d(n + k))
// Optimized: ping-pong buffers (no memcpy)
// ==============================================================
void counting_sort_to(int *src, int *dst, int n, int k, int digit) {
  int divisor = 1;
  for (int i = 0; i < digit; i++)
    divisor *= k;

  int *C = (int *)calloc(k, sizeof(int));

  for (int i = 0; i < n; i++) {
    int x = (src[i] / divisor) % k;
    C[x]++;
  }

  for (int i = 1; i < k; i++) {
    C[i] += C[i - 1];
  }

  for (int i = n - 1; i >= 0; i--) {
    int x = (src[i] / divisor) % k;
    dst[C[x] - 1] = src[i];
    C[x]--;
  }

  free(C);
}

void radix_sort(int *A, int n, int d, int k) {
  int *B = (int *)malloc(n * sizeof(int));
  int *src = A;
  int *dst = B;

  for (int digit = 0; digit < d; digit++) {
    counting_sort_to(src, dst, n, k, digit);
    int *tmp = src;
    src = dst;
    dst = tmp;
  }

  if (src != A) {
    memcpy(A, src, n * sizeof(int));
  }

  free(B);
}

// ==============================================================
// BUCKET SORT - O(n) average (assumes uniform distribution)
// Adapted for integers in [0, max_val)
// ==============================================================
typedef struct {
  int *data;
  int size;
  int capacity;
} Bucket;

void bucket_insert(Bucket *b, int val) {
  if (b->size >= b->capacity) {
    b->capacity = b->capacity == 0 ? 4 : b->capacity * 2;
    b->data = (int *)realloc(b->data, b->capacity * sizeof(int));
  }
  b->data[b->size++] = val;
}

void bucket_insertion_sort(Bucket *b) {
  for (int i = 1; i < b->size; i++) {
    int key = b->data[i];
    int j = i - 1;
    while (j >= 0 && b->data[j] > key) {
      b->data[j + 1] = b->data[j];
      j--;
    }
    b->data[j + 1] = key;
  }
}

void bucket_sort(int *A, int n, int max_val) {
  Bucket *buckets = (Bucket *)calloc(n, sizeof(Bucket));

  // Distribute elements into buckets
  for (int i = 0; i < n; i++) {
    // Map [0, max_val) -> [0, n)
    int idx = (int)((long long)A[i] * n / max_val);
    if (idx >= n)
      idx = n - 1; // Handle edge case
    bucket_insert(&buckets[idx], A[i]);
  }

  // Sort each bucket and concatenate
  int out_idx = 0;
  for (int i = 0; i < n; i++) {
    if (buckets[i].size > 0) {
      bucket_insertion_sort(&buckets[i]);
      for (int j = 0; j < buckets[i].size; j++) {
        A[out_idx++] = buckets[i].data[j];
      }
      free(buckets[i].data);
    }
  }

  free(buckets);
}

// ==============================================================
// UTILITY FUNCTIONS
// ==============================================================
bool is_sorted(int *A, int n) {
  for (int i = 0; i < n - 1; i++) {
    if (A[i] > A[i + 1])
      return false;
  }
  return true;
}

void fill_random(int *A, int n, int max_val) {
  for (int i = 0; i < n; i++) {
    A[i] = rand() % max_val;
  }
}

int *copy_array(int *A, int n) {
  int *B = (int *)malloc(n * sizeof(int));
  memcpy(B, A, n * sizeof(int));
  return B;
}

int num_digits(int max_val, int base) {
  int d = 0;
  while (max_val > 0) {
    max_val /= base;
    d++;
  }
  return d;
}

// ==============================================================
// BENCHMARKING (with cache warming)
// ==============================================================
#define WARMUP_RUNS 2
#define TIMED_RUNS 5

typedef struct {
  double insertion_ms;
  double quicksort_ms;
  double radix_ms;
  double bucket_ms;
  int size;
  bool insertion_correct;
  bool quicksort_correct;
  bool radix_correct;
  bool bucket_correct;
} BenchmarkResult;

double time_ms(clock_t start, clock_t end) {
  return ((double)(end - start)) / CLOCKS_PER_SEC * 1000.0;
}

int cmp_double(const void *a, const void *b) {
  double da = *(const double *)a;
  double db = *(const double *)b;
  return (da > db) - (da < db);
}

double median_time(double *times, int count) {
  qsort(times, count, sizeof(double), cmp_double);
  return times[count / 2];
}

BenchmarkResult benchmark(int size, int max_val, bool run_insertion) {
  BenchmarkResult result = {0};
  result.size = size;

  int *original = (int *)malloc(size * sizeof(int));
  fill_random(original, size, max_val);

  int d = num_digits(max_val, 10);
  clock_t start, end;
  double times[TIMED_RUNS];

  // ============ Insertion Sort ============
  if (run_insertion) {
    for (int w = 0; w < WARMUP_RUNS; w++) {
      int *arr = copy_array(original, size);
      insertion_sort(arr, size);
      free(arr);
    }
    for (int r = 0; r < TIMED_RUNS; r++) {
      int *arr = copy_array(original, size);
      start = clock();
      insertion_sort(arr, size);
      end = clock();
      times[r] = time_ms(start, end);
      result.insertion_correct = is_sorted(arr, size);
      free(arr);
    }
    result.insertion_ms = median_time(times, TIMED_RUNS);
  } else {
    result.insertion_ms = -1;
    result.insertion_correct = true;
  }

  // ============ Quicksort ============
  {
    for (int w = 0; w < WARMUP_RUNS; w++) {
      int *arr = copy_array(original, size);
      quicksort(arr, size);
      free(arr);
    }
    for (int r = 0; r < TIMED_RUNS; r++) {
      int *arr = copy_array(original, size);
      start = clock();
      quicksort(arr, size);
      end = clock();
      times[r] = time_ms(start, end);
      result.quicksort_correct = is_sorted(arr, size);
      free(arr);
    }
    result.quicksort_ms = median_time(times, TIMED_RUNS);
  }

  // ============ Radix Sort ============
  {
    for (int w = 0; w < WARMUP_RUNS; w++) {
      int *arr = copy_array(original, size);
      radix_sort(arr, size, d, 10);
      free(arr);
    }
    for (int r = 0; r < TIMED_RUNS; r++) {
      int *arr = copy_array(original, size);
      start = clock();
      radix_sort(arr, size, d, 10);
      end = clock();
      times[r] = time_ms(start, end);
      result.radix_correct = is_sorted(arr, size);
      free(arr);
    }
    result.radix_ms = median_time(times, TIMED_RUNS);
  }

  // ============ Bucket Sort ============
  {
    for (int w = 0; w < WARMUP_RUNS; w++) {
      int *arr = copy_array(original, size);
      bucket_sort(arr, size, max_val);
      free(arr);
    }
    for (int r = 0; r < TIMED_RUNS; r++) {
      int *arr = copy_array(original, size);
      start = clock();
      bucket_sort(arr, size, max_val);
      end = clock();
      times[r] = time_ms(start, end);
      result.bucket_correct = is_sorted(arr, size);
      free(arr);
    }
    result.bucket_ms = median_time(times, TIMED_RUNS);
  }

  free(original);
  return result;
}

// ==============================================================
// MAIN
// ==============================================================
// clang-format off
int main() {
  srand(42);

  printf("\n");
  printf("┌─────────────────────────────────────────────────────────────────────────────────┐\n");
  printf("│                         SORTING ALGORITHM BENCHMARK                             │\n");
  printf("│                         Values: 0 to 999,999 (uniform)                          │\n");
  printf("│                         Median of %d runs, %d warmup runs                        │\n", TIMED_RUNS, WARMUP_RUNS);
  printf("├─────────────┬────────────────┬──────────────┬──────────────┬────────────────────┤\n");
  printf("│  Array Size │ Insertion Sort │   Quicksort  │  Radix Sort  │    Bucket Sort     │\n");
  printf("├─────────────┼────────────────┼──────────────┼──────────────┼────────────────────┤\n");

  int sizes[] = {1000, 5000, 10000, 50000, 100000, 500000, 1000000};
  int num_sizes = sizeof(sizes) / sizeof(sizes[0]);
  int max_val = 1000000;

  for (int i = 0; i < num_sizes; i++) {
    int size = sizes[i];
    bool run_insertion = (size <= 50000);

    BenchmarkResult r = benchmark(size, max_val, run_insertion);

    char insertion_str[16];
    if (r.insertion_ms < 0) {
      snprintf(insertion_str, 16, "  (skipped)");
    } else {
      snprintf(insertion_str, 16, "%8.2f ms", r.insertion_ms);
    }

    printf("│ %10d  │ %14s │ %9.2f ms │ %9.2f ms │ %12.2f ms     │\n",
           r.size, insertion_str, r.quicksort_ms, r.radix_ms, r.bucket_ms);
  }

  printf("├─────────────┴────────────────┴──────────────┴──────────────┴────────────────────┤\n");
  printf("│  Note: Insertion sort skipped for n > 50,000 (too slow)                         │\n");
  printf("└─────────────────────────────────────────────────────────────────────────────────┘\n");

  printf("\n");
  printf("┌──────────────────┬──────────────────┬──────────┬─────────┬──────────────────────┐\n");
  printf("│ Algorithm        │ Time Complexity  │  Space   │ Stable? │ Notes                │\n");
  printf("├──────────────────┼──────────────────┼──────────┼─────────┼──────────────────────┤\n");
  printf("│ Insertion Sort   │ O(n²)            │ O(1)     │   Yes   │ Simple               │\n");
  printf("│ Quicksort        │ O(n log n) avg   │ O(log n) │   No    │ Fast general-purpose │\n");
  printf("│ Radix Sort       │ O(d(n + k))      │ O(n + k) │   Yes   │ Linear for fixed d   │\n");
  printf("│ Bucket Sort      │ O(n) avg         │ O(n)     │   Yes   │ Needs uniform dist.  │\n");
  printf("└──────────────────┴──────────────────┴──────────┴─────────┴──────────────────────┘\n");

  printf("\n");
  printf("Methodology:\n");
  printf("  • %d warmup runs (cache warming)\n", WARMUP_RUNS);
  printf("  • %d timed runs (median reported)\n", TIMED_RUNS);
  printf("  • Inlined swap in quicksort\n");
  printf("  • Radix uses ping-pong buffers\n");
  printf("  • Uniform random distribution\n\n");

  return 0;
}
// clang-format on
