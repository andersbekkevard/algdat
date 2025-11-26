

// ==============================================================
// QUICKSORT - O(n log n) average, O(n²) worst
// Inlined swap for fair comparison
// ==============================================================
int partition(int *A, int lo, int hi) {
  int pivot = A[hi];
  int i = lo - 1;