/*
 * Benchmark: Heapsort vs Mergesort vs Quicksort in C
 * Goal: Visualize the constant factor in O(n log n) without interpreter
 * overhead
 *
 * Compile: gcc -O2 -o sorting_benchmark sorting_benchmark.c -lm
 * Run:     ./sorting_benchmark
 */

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// ============================================================================
// HEAPSORT (in-place)
// ============================================================================

static inline void swap(int *a, int *b) {
  int tmp = *a;
  *a = *b;
  *b = tmp;
}

static void max_heapify(int *A, int size, int i) {
  int greatest = i;
  int l = 2 * i + 1;
  int r = 2 * i + 2;

  if (l < size && A[l] > A[greatest])
    greatest = l;
  if (r < size && A[r] > A[greatest])
    greatest = r;

  if (greatest != i) {
    swap(&A[i], &A[greatest]);
    max_heapify(A, size, greatest);
  }
}

void heap_sort(int *A, int n) {
  if (n <= 1)
    return;

  // Build max-heap (bottom-up)
  for (int i = (n - 2) / 2; i >= 0; i--) {
    max_heapify(A, n, i);
  }

  // Extract elements one by one
  for (int heap_size = n - 1; heap_size > 0; heap_size--) {
    swap(&A[0], &A[heap_size]);
    max_heapify(A, heap_size, 0);
  }
}

// ============================================================================
// MERGESORT (with auxiliary array)
// ============================================================================

static int *aux = NULL; // Pre-allocated auxiliary array

static void merge(int *A, int lo, int mid, int hi) {
  // Copy to aux
  for (int k = lo; k <= hi; k++) {
    aux[k] = A[k];
  }

  int i = lo, j = mid + 1;
  for (int k = lo; k <= hi; k++) {
    if (i > mid) {
      A[k] = aux[j++];
    } else if (j > hi) {
      A[k] = aux[i++];
    } else if (aux[i] <= aux[j]) {
      A[k] = aux[i++];
    } else {
      A[k] = aux[j++];
    }
  }
}

static void mergesort_recursive(int *A, int lo, int hi) {
  if (lo >= hi)
    return;
  int mid = lo + (hi - lo) / 2;
  mergesort_recursive(A, lo, mid);
  mergesort_recursive(A, mid + 1, hi);
  merge(A, lo, mid, hi);
}

void merge_sort(int *A, int n) {
  if (n <= 1)
    return;
  aux = (int *)malloc(n * sizeof(int));
  mergesort_recursive(A, 0, n - 1);
  free(aux);
  aux = NULL;
}

// ============================================================================
// QUICKSORT (in-place, median-of-three pivot)
// ============================================================================

static int median_of_three(int *A, int lo, int hi) {
  int mid = lo + (hi - lo) / 2;
  if (A[lo] > A[mid])
    swap(&A[lo], &A[mid]);
  if (A[lo] > A[hi])
    swap(&A[lo], &A[hi]);
  if (A[mid] > A[hi])
    swap(&A[mid], &A[hi]);
  return mid;
}

static int partition(int *A, int lo, int hi) {
  int pivot_idx = median_of_three(A, lo, hi);
  swap(&A[pivot_idx], &A[hi]); // Move pivot to end
  int pivot = A[hi];

  int i = lo - 1;
  for (int j = lo; j < hi; j++) {
    if (A[j] <= pivot) {
      i++;
      swap(&A[i], &A[j]);
    }
  }
  swap(&A[i + 1], &A[hi]);
  return i + 1;
}

static void quicksort_recursive(int *A, int lo, int hi) {
  if (lo >= hi)
    return;
  int p = partition(A, lo, hi);
  quicksort_recursive(A, lo, p - 1);
  quicksort_recursive(A, p + 1, hi);
}

void quick_sort(int *A, int n) {
  if (n <= 1)
    return;
  quicksort_recursive(A, 0, n - 1);
}

// ============================================================================
// BENCHMARKING
// ============================================================================

typedef void (*SortFunc)(int *, int);

// High-resolution timer
double get_time_sec(void) {
  struct timespec ts;
  clock_gettime(CLOCK_MONOTONIC, &ts);
  return ts.tv_sec + ts.tv_nsec / 1e9;
}

// Generate random array
void fill_random(int *A, int n, unsigned int seed) {
  srand(seed);
  for (int i = 0; i < n; i++) {
    A[i] = rand() % (n * 10);
  }
}

// Verify array is sorted
int is_sorted(int *A, int n) {
  for (int i = 1; i < n; i++) {
    if (A[i] < A[i - 1])
      return 0;
  }
  return 1;
}

double benchmark_sort(SortFunc sort_func, int n, int trials,
                      unsigned int base_seed) {
  int *data = (int *)malloc(n * sizeof(int));
  double total_time = 0.0;

  for (int trial = 0; trial < trials; trial++) {
    fill_random(data, n, base_seed + trial);

    double start = get_time_sec();
    sort_func(data, n);
    double end = get_time_sec();

    total_time += (end - start);

    // Verify correctness
    if (!is_sorted(data, n)) {
      fprintf(stderr, "ERROR: Array not sorted for n=%d, trial=%d\n", n, trial);
    }
  }

  free(data);
  return total_time / trials;
}

double compute_constant(int n, double time_sec) {
  if (n <= 1)
    return 0.0;
  return time_sec / (n * log2((double)n));
}

int main(void) {
  int sizes[] = {100,   500,    1000,   5000,    10000,
                 50000, 100000, 500000, 1000000, 5000000};
  int num_sizes = sizeof(sizes) / sizeof(sizes[0]);
  int trials = 5;
  unsigned int seed = 42;

  printf("Benchmarking sorting algorithms (C implementation)\n");
  printf("Trials per size: %d\n", trials);
  printf("Compiler optimizations: -O2\n\n");

  // Header
  printf("====================================================================="
         "=============================\n");
  printf("%12s | %18s | %18s | %18s\n", "SIZE", "HEAPSORT", "MERGESORT",
         "QUICKSORT");
  printf("%12s | %8s %8s | %8s %8s | %8s %8s\n", "", "time(ms)", "const",
         "time(ms)", "const", "time(ms)", "const");
  printf("====================================================================="
         "=============================\n");

  double heap_consts[10], merge_consts[10], quick_consts[10];
  int large_count = 0;

  for (int i = 0; i < num_sizes; i++) {
    int n = sizes[i];

    double heap_t = benchmark_sort(heap_sort, n, trials, seed);
    double merge_t = benchmark_sort(merge_sort, n, trials, seed);
    double quick_t = benchmark_sort(quick_sort, n, trials, seed);

    double heap_c = compute_constant(n, heap_t) * 1e9; // nanoseconds
    double merge_c = compute_constant(n, merge_t) * 1e9;
    double quick_c = compute_constant(n, quick_t) * 1e9;

    printf("%12d | %8.3f %8.2f | %8.3f %8.2f | %8.3f %8.2f\n", n, heap_t * 1000,
           heap_c, merge_t * 1000, merge_c, quick_t * 1000, quick_c);

    // Collect constants for n >= 1000
    if (n >= 1000) {
      heap_consts[large_count] = heap_c;
      merge_consts[large_count] = merge_c;
      quick_consts[large_count] = quick_c;
      large_count++;
    }
  }

  printf("====================================================================="
         "=============================\n");
  printf("Note: 'const' = time / (n * log2(n)) in nanoseconds\n");
  printf(
      "      A stable constant across sizes confirms O(n log n) behavior\n\n");

  // Compute averages
  double avg_heap = 0, avg_merge = 0, avg_quick = 0;
  for (int i = 0; i < large_count; i++) {
    avg_heap += heap_consts[i];
    avg_merge += merge_consts[i];
    avg_quick += quick_consts[i];
  }
  avg_heap /= large_count;
  avg_merge /= large_count;
  avg_quick /= large_count;

  printf("Average constants (for n >= 1000):\n");
  printf("  Heapsort:  %.2f ns\n", avg_heap);
  printf("  Mergesort: %.2f ns\n", avg_merge);
  printf("  Quicksort: %.2f ns\n", avg_quick);

  double fastest = avg_quick;
  if (avg_heap < fastest)
    fastest = avg_heap;
  if (avg_merge < fastest)
    fastest = avg_merge;

  printf("\nRelative to fastest:\n");
  printf("  Heapsort:  %.2fx\n", avg_heap / fastest);
  printf("  Mergesort: %.2fx\n", avg_merge / fastest);
  printf("  Quicksort: %.2fx\n", avg_quick / fastest);

  return 0;
}
