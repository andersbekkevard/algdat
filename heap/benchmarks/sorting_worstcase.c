/*
 * Benchmark: Quicksort (naive last-element pivot) vs Heapsort vs Mergesort
 * on different input distributions: random, sorted, reverse-sorted, etc.
 *
 * Compile: gcc -O2 -o sorting_worstcase sorting_worstcase.c -lm
 * Run:     ./sorting_worstcase
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// ============================================================================
// SORTING ALGORITHMS
// ============================================================================

static inline void swap(int *a, int *b) {
  int tmp = *a;
  *a = *b;
  *b = tmp;
}

// --- HEAPSORT ---
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
  for (int i = (n - 2) / 2; i >= 0; i--)
    max_heapify(A, n, i);
  for (int s = n - 1; s > 0; s--) {
    swap(&A[0], &A[s]);
    max_heapify(A, s, 0);
  }
}

// --- MERGESORT ---
static int *aux = NULL;

static void merge(int *A, int lo, int mid, int hi) {
  for (int k = lo; k <= hi; k++)
    aux[k] = A[k];
  int i = lo, j = mid + 1;
  for (int k = lo; k <= hi; k++) {
    if (i > mid)
      A[k] = aux[j++];
    else if (j > hi)
      A[k] = aux[i++];
    else if (aux[i] <= aux[j])
      A[k] = aux[i++];
    else
      A[k] = aux[j++];
  }
}

static void ms_rec(int *A, int lo, int hi) {
  if (lo >= hi)
    return;
  int mid = lo + (hi - lo) / 2;
  ms_rec(A, lo, mid);
  ms_rec(A, mid + 1, hi);
  merge(A, lo, mid, hi);
}

void merge_sort(int *A, int n) {
  if (n <= 1)
    return;
  aux = malloc(n * sizeof(int));
  ms_rec(A, 0, n - 1);
  free(aux);
  aux = NULL;
}

// --- QUICKSORT NAIVE (last element pivot) ---
static int part_naive(int *A, int lo, int hi) {
  int pivot = A[hi], i = lo - 1;
  for (int j = lo; j < hi; j++)
    if (A[j] <= pivot)
      swap(&A[++i], &A[j]);
  swap(&A[i + 1], &A[hi]);
  return i + 1;
}

static void qs_naive_rec(int *A, int lo, int hi) {
  if (lo >= hi)
    return;
  int p = part_naive(A, lo, hi);
  qs_naive_rec(A, lo, p - 1);
  qs_naive_rec(A, p + 1, hi);
}

void quick_sort_naive(int *A, int n) {
  if (n <= 1)
    return;
  qs_naive_rec(A, 0, n - 1);
}

// --- QUICKSORT GOOD (median-of-three pivot) ---
static int median3(int *A, int lo, int hi) {
  int mid = lo + (hi - lo) / 2;
  if (A[lo] > A[mid])
    swap(&A[lo], &A[mid]);
  if (A[lo] > A[hi])
    swap(&A[lo], &A[hi]);
  if (A[mid] > A[hi])
    swap(&A[mid], &A[hi]);
  return mid;
}

static int part_good(int *A, int lo, int hi) {
  swap(&A[median3(A, lo, hi)], &A[hi]);
  int pivot = A[hi], i = lo - 1;
  for (int j = lo; j < hi; j++)
    if (A[j] <= pivot)
      swap(&A[++i], &A[j]);
  swap(&A[i + 1], &A[hi]);
  return i + 1;
}

static void qs_good_rec(int *A, int lo, int hi) {
  if (lo >= hi)
    return;
  int p = part_good(A, lo, hi);
  qs_good_rec(A, lo, p - 1);
  qs_good_rec(A, p + 1, hi);
}

void quick_sort_good(int *A, int n) {
  if (n <= 1)
    return;
  qs_good_rec(A, 0, n - 1);
}

// ============================================================================
// INPUT GENERATORS (all take seed for uniform interface)
// ============================================================================

void fill_random(int *A, int n, unsigned s) {
  srand(s);
  for (int i = 0; i < n; i++)
    A[i] = rand() % (n * 10);
}
void fill_sorted(int *A, int n, unsigned s) {
  (void)s;
  for (int i = 0; i < n; i++)
    A[i] = i;
}
void fill_reverse(int *A, int n, unsigned s) {
  (void)s;
  for (int i = 0; i < n; i++)
    A[i] = n - i;
}
void fill_all_equal(int *A, int n, unsigned s) {
  (void)s;
  for (int i = 0; i < n; i++)
    A[i] = 42;
}
void fill_nearly_sorted(int *A, int n, unsigned s) {
  for (int i = 0; i < n; i++)
    A[i] = i;
  srand(s);
  for (int i = 0; i < n / 20; i++) {
    int a = rand() % n, b = rand() % n;
    swap(&A[a], &A[b]);
  }
}
void fill_80_sorted(int *A, int n, unsigned s) {
  int cut = (int)(n * 0.8);
  for (int i = 0; i < cut; i++)
    A[i] = i;
  srand(s);
  for (int i = cut; i < n; i++)
    A[i] = rand() % (n * 10);
}

// ============================================================================
// BENCHMARK INFRASTRUCTURE
// ============================================================================

typedef void (*SortFn)(int *, int);
typedef void (*FillFn)(int *, int, unsigned);

static double now(void) {
  struct timespec ts;
  clock_gettime(CLOCK_MONOTONIC, &ts);
  return ts.tv_sec + ts.tv_nsec / 1e9;
}

static int sorted(int *A, int n) {
  for (int i = 1; i < n; i++)
    if (A[i] < A[i - 1])
      return 0;
  return 1;
}

static double bench(SortFn sort, int *buf, int n, int trials, FillFn fill,
                    unsigned seed) {
  double t = 0;
  for (int i = 0; i < trials; i++) {
    fill(buf, n, seed + i);
    double s = now();
    sort(buf, n);
    t += now() - s;
    if (!sorted(buf, n))
      fprintf(stderr, "ERROR: not sorted!\n");
  }
  return t / trials;
}

// ============================================================================
// TEST CONFIGURATION
// ============================================================================

#define TRIALS 3
#define SEED 42
static int SIZES[] = {1000, 5000, 10000, 20000, 50000};
#define NUM_SIZES (sizeof(SIZES) / sizeof(SIZES[0]))

// Threshold for skipping naive QS (stack overflow on sorted)
#define NAIVE_MAX 10000

// ============================================================================
// TEST FUNCTIONS - COMMENT/UNCOMMENT THESE IN main()
// ============================================================================

void test_random(int *buf, int n) {
  double h = bench(heap_sort, buf, n, TRIALS, fill_random, SEED);
  double m = bench(merge_sort, buf, n, TRIALS, fill_random, SEED);
  double qn = bench(quick_sort_naive, buf, n, TRIALS, fill_random, SEED);
  double qg = bench(quick_sort_good, buf, n, TRIALS, fill_random, SEED);
  printf("  %-14s | %8.2f | %8.2f | %8.2f | %8.2f\n", "Random", h * 1000,
         m * 1000, qn * 1000, qg * 1000);
}

void test_sorted(int *buf, int n) {
  double h = bench(heap_sort, buf, n, TRIALS, fill_sorted, SEED);
  double m = bench(merge_sort, buf, n, TRIALS, fill_sorted, SEED);
  double qg = bench(quick_sort_good, buf, n, TRIALS, fill_sorted, SEED);
  if (n <= NAIVE_MAX) {
    double qn = bench(quick_sort_naive, buf, n, TRIALS, fill_sorted, SEED);
    printf("  %-14s | %8.2f | %8.2f | %8.2f | %8.2f\n", "Sorted", h * 1000,
           m * 1000, qn * 1000, qg * 1000);
  } else {
    printf("  %-14s | %8.2f | %8.2f | %8s | %8.2f\n", "Sorted", h * 1000,
           m * 1000, "OVERFLOW", qg * 1000);
  }
}

void test_reverse(int *buf, int n) {
  double h = bench(heap_sort, buf, n, TRIALS, fill_reverse, SEED);
  double m = bench(merge_sort, buf, n, TRIALS, fill_reverse, SEED);
  double qg = bench(quick_sort_good, buf, n, TRIALS, fill_reverse, SEED);
  if (n <= NAIVE_MAX) {
    double qn = bench(quick_sort_naive, buf, n, TRIALS, fill_reverse, SEED);
    printf("  %-14s | %8.2f | %8.2f | %8.2f | %8.2f\n", "Reverse", h * 1000,
           m * 1000, qn * 1000, qg * 1000);
  } else {
    printf("  %-14s | %8.2f | %8.2f | %8s | %8.2f\n", "Reverse", h * 1000,
           m * 1000, "OVERFLOW", qg * 1000);
  }
}

void test_nearly_sorted(int *buf, int n) {
  double h = bench(heap_sort, buf, n, TRIALS, fill_nearly_sorted, SEED);
  double m = bench(merge_sort, buf, n, TRIALS, fill_nearly_sorted, SEED);
  double qn = bench(quick_sort_naive, buf, n, TRIALS, fill_nearly_sorted, SEED);
  double qg = bench(quick_sort_good, buf, n, TRIALS, fill_nearly_sorted, SEED);
  printf("  %-14s | %8.2f | %8.2f | %8.2f | %8.2f\n", "Nearly sorted", h * 1000,
         m * 1000, qn * 1000, qg * 1000);
}

void test_80_sorted(int *buf, int n) {
  double h = bench(heap_sort, buf, n, TRIALS, fill_80_sorted, SEED);
  double m = bench(merge_sort, buf, n, TRIALS, fill_80_sorted, SEED);
  double qn = bench(quick_sort_naive, buf, n, TRIALS, fill_80_sorted, SEED);
  double qg = bench(quick_sort_good, buf, n, TRIALS, fill_80_sorted, SEED);
  printf("  %-14s | %8.2f | %8.2f | %8.2f | %8.2f\n", "80%% sorted", h * 1000,
         m * 1000, qn * 1000, qg * 1000);
}

void test_all_equal(int *buf, int n) {
  // MEDIAN-OF-THREE KILLER: all equal → O(n²) even with good pivot!
  double h = bench(heap_sort, buf, n, TRIALS, fill_all_equal, SEED);
  double m = bench(merge_sort, buf, n, TRIALS, fill_all_equal, SEED);
  double qn = (n <= NAIVE_MAX) ? bench(quick_sort_naive, buf, n, TRIALS,
                                       fill_all_equal, SEED)
                               : -1;
  double qg = (n <= NAIVE_MAX)
                  ? bench(quick_sort_good, buf, n, TRIALS, fill_all_equal, SEED)
                  : -1;
  if (qn < 0)
    printf("  %-14s | %8.2f | %8.2f | %8s | %8s\n", "All equal", h * 1000,
           m * 1000, "OVERFLOW", "OVERFLOW");
  else
    printf("  %-14s | %8.2f | %8.2f | %8.2f | %8.2f\n", "All equal", h * 1000,
           m * 1000, qn * 1000, qg * 1000);
}

void print_header(int n) {
  printf("─────────────────────────────────────────────────────────────────────"
         "\n");
  printf("n = %d\n", n);
  printf("─────────────────────────────────────────────────────────────────────"
         "\n");
  printf("  %-14s | %8s | %8s | %8s | %8s\n", "Input", "Heap", "Merge",
         "QS-Naive", "QS-Good");
  printf("  %-14s | %8s | %8s | %8s | %8s\n", "", "(ms)", "(ms)", "(ms)",
         "(ms)");
}

void run_tests_for_size(int n) {
  int *buf = malloc(n * sizeof(int));
  print_header(n);

  // =========================================================
  // COMMENT/UNCOMMENT INDIVIDUAL TESTS HERE:
  // =========================================================
  test_random(buf, n);
  test_sorted(buf, n);
  test_reverse(buf, n);
  test_nearly_sorted(buf, n);
  test_80_sorted(buf, n);
  // test_all_equal(buf, n);  // ← UNCOMMENT FOR MEDIAN-OF-THREE KILLER
  // =========================================================

  printf("\n");
  free(buf);
}

// ============================================================================
// MAIN - COMMENT/UNCOMMENT SIZES HERE
// ============================================================================

int main(void) {
  printf(
      "Sorting Benchmark: QS-Naive (last elem) vs QS-Good (median-of-3)\n\n");

  for (int i = 0; i < (int)NUM_SIZES; i++)
    run_tests_for_size(SIZES[i]);

  return 0;
}
