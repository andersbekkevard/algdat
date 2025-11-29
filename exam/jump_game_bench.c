/*
 * Benchmark: Minimum Jumps Problem
 *
 * Three strategies:
 *   1. solve_dp      - Dynamic programming O(n*s)
 *   2. solve_bfs     - BFS on implicit graph O(n*s)
 *   3. solve_greedy  - Linear greedy O(n)
 *
 * Compile: gcc -O3 -o jump_game_bench jump_game_bench.c
 * Run:     ./jump_game_bench
 */

#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_N 100000
#define MAX_STEP 5

// Set to 1 to preallocate arrays (removes malloc overhead from benchmark)
// Set to 0 for realistic benchmark including allocation costs
#define PREALLOC_ARRAYS 1

#if PREALLOC_ARRAYS
static int *g_dp = NULL;
static int *g_dist = NULL;
static int *g_queue = NULL;
#endif

// ==================================
// Solution 1: Dynamic Programming (backwards)
// Time: O(n * s), Space: O(n)
// ==================================
int solve_dp(int *board, int n) {
#if PREALLOC_ARRAYS
  int *dp = g_dp;
#else
  int *dp = malloc(n * sizeof(int));
#endif

  dp[n - 1] = 0;
  for (int i = n - 2; i >= 0; i--) {
    dp[i] = INT_MAX - 1;
    for (int s = 1; s <= board[i] && i + s < n; s++) {
      if (dp[i + s] + 1 < dp[i]) {
        dp[i] = dp[i + s] + 1;
      }
    }
  }

  int result = dp[0];
#if !PREALLOC_ARRAYS
  free(dp);
#endif
  return result;
}

// ==================================
// Solution 2: BFS on implicit graph
// Time: O(n * s), Space: O(n)
// ==================================
int solve_bfs(int *board, int n) {
#if PREALLOC_ARRAYS
  int *dist = g_dist;
  int *queue = g_queue;
#else
  int *dist = malloc(n * sizeof(int));
  int *queue = malloc(n * sizeof(int));
#endif

  memset(dist, -1, n * sizeof(int));
  dist[0] = 0;

  int head = 0, tail = 0;
  queue[tail++] = 0;

  while (head < tail) {
    int pos = queue[head++];

    for (int step = 1; step <= board[pos]; step++) {
      int next = pos + step;
      if (next >= n)
        break;

      if (dist[next] == -1) {
        dist[next] = dist[pos] + 1;
        if (next == n - 1) {
#if !PREALLOC_ARRAYS
          free(dist);
          free(queue);
#endif
          return dist[next];
        }
        queue[tail++] = next;
      }
    }
  }

  int result = dist[n - 1];
#if !PREALLOC_ARRAYS
  free(dist);
  free(queue);
#endif
  return result;
}

// ==================================
// Solution 3: Greedy (linear time)
// Time: O(n), Space: O(1)
// ==================================
int solve_greedy(int *board, int n) {
  if (n <= 1)
    return 0;

  int jumps = 1;
  int steps_left = board[0];
  int max_reach = board[0];

  for (int i = 1; i < n - 1; i++) {
    steps_left--;
    if (i + board[i] > max_reach) {
      max_reach = i + board[i];
    }
    if (steps_left == 0) {
      steps_left = max_reach - i;
      jumps++;
    }
  }

  return jumps;
}

// ==================================
// Test & Benchmark Utilities
// ==================================

void generate_board_with_step(int *board, int n, int max_step) {
  for (int i = 0; i < n - 1; i++) {
    int remaining = n - 1 - i;
    int max_jump = remaining < max_step ? remaining : max_step;
    board[i] = 1 + rand() % max_jump;
  }
  board[n - 1] = 0;
}

void generate_board(int *board, int n) {
  generate_board_with_step(board, n, MAX_STEP);
}

double benchmark(int (*solver)(int *, int), int *board, int n, int runs) {
  // Warmup
  for (int r = 0; r < 10; r++) {
    solver(board, n);
  }

  clock_t start = clock();
  for (int r = 0; r < runs; r++) {
    volatile int result = solver(board, n); // volatile prevents optimization
    (void)result;
  }
  clock_t end = clock();

  return ((double)(end - start) / CLOCKS_PER_SEC / runs) * 1000.0; // ms
}

void print_separator(int col_width) {
  printf("+----------+");
  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < col_width; j++)
      printf("-");
    printf(i < 2 ? "+" : "+\n");
  }
}

void print_header(int col_width) {
  printf("\n+----------+");
  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < col_width; j++)
      printf("-");
    printf(i < 2 ? "+" : "+\n");
  }

  printf("|%10s|%*s|%*s|%*s|\n", "n", col_width, "solve_dp", col_width,
         "solve_bfs", col_width, "solve_greedy");

  print_separator(col_width);
}

void print_footer(int col_width) {
  printf("+----------+");
  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < col_width; j++)
      printf("-");
    printf(i < 2 ? "+" : "+\n");
  }
}

void format_time(char *buf, double t, int is_fastest) {
  const char *prefix = is_fastest ? "*" : " ";
  double us = t * 1000.0; // convert ms to us
  if (us < 10) {
    sprintf(buf, "%s%.2f us", prefix, us);
  } else if (us < 100) {
    sprintf(buf, "%s%.1f us", prefix, us);
  } else {
    sprintf(buf, "%s%.0f us", prefix, us);
  }
}

void print_row(int n, double t1, double t2, double t3, int col_width) {
  double min_t = t1 < t2 ? (t1 < t3 ? t1 : t3) : (t2 < t3 ? t2 : t3);

  char buf1[32], buf2[32], buf3[32];
  format_time(buf1, t1, t1 == min_t);
  format_time(buf2, t2, t2 == min_t);
  format_time(buf3, t3, t3 == min_t);

  printf("|%10d|%*s|%*s|%*s|\n", n, col_width, buf1, col_width, buf2, col_width,
         buf3);
}

// Header for step benchmark (s instead of n)
void print_header_step(int col_width) {
  printf("\n+----------+");
  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < col_width; j++)
      printf("-");
    printf(i < 2 ? "+" : "+\n");
  }

  printf("|%10s|%*s|%*s|%*s|\n", "s", col_width, "solve_dp", col_width,
         "solve_bfs", col_width, "solve_greedy");

  print_separator(col_width);
}

void print_row_step(int s, double t1, double t2, double t3, int col_width) {
  double min_t = t1 < t2 ? (t1 < t3 ? t1 : t3) : (t2 < t3 ? t2 : t3);

  char buf1[32], buf2[32], buf3[32];
  format_time(buf1, t1, t1 == min_t);
  format_time(buf2, t2, t2 == min_t);
  format_time(buf3, t3, t3 == min_t);

  printf("|%10d|%*s|%*s|%*s|\n", s, col_width, buf1, col_width, buf2, col_width,
         buf3);
}

int main() {
  srand(42);

  int sizes[] = {100, 1000, 10000, 50000, 100000};
  int num_sizes = sizeof(sizes) / sizeof(sizes[0]);
  int runs = 1000;
  int col_width = 16;

  int *board = malloc(MAX_N * sizeof(int));

#if PREALLOC_ARRAYS
  g_dp = malloc(MAX_N * sizeof(int));
  g_dist = malloc(MAX_N * sizeof(int));
  g_queue = malloc(MAX_N * sizeof(int));
#endif

  printf("\n");
  printf("  +-----------------------------------------------------------+\n");
  printf("  |         JUMP GAME BENCHMARK (C Implementation)           |\n");
#if PREALLOC_ARRAYS
  printf("  |  Mode: PREALLOC (no malloc in benchmark)                  |\n");
#else
  printf("  |  Mode: REALISTIC (includes malloc/free overhead)         |\n");
#endif
  printf("  |  solve_dp: O(n*s)   solve_bfs: O(n*s)   solve_greedy: O(n) |\n");
  printf("  +-----------------------------------------------------------+\n");

  print_header(col_width);

  double results[5][3];

  for (int i = 0; i < num_sizes; i++) {
    int n = sizes[i];
    generate_board(board, n);

    // Verify correctness
    int r1 = solve_dp(board, n);
    int r2 = solve_bfs(board, n);
    int r3 = solve_greedy(board, n);

    if (r1 != r2 || r2 != r3) {
      printf("ERROR: Results differ! dp=%d, bfs=%d, greedy=%d\n", r1, r2, r3);
      continue;
    }

    double t1 = benchmark(solve_dp, board, n, runs);
    double t2 = benchmark(solve_bfs, board, n, runs);
    double t3 = benchmark(solve_greedy, board, n, runs);

    results[i][0] = t1;
    results[i][1] = t2;
    results[i][2] = t3;

    print_row(n, t1, t2, t3, col_width);
  }

  print_footer(col_width);

  // Speedup summary
  printf("\n  Speedup vs solve_dp:\n");
  for (int i = 0; i < num_sizes; i++) {
    double bfs_speedup = results[i][0] / results[i][1];
    double greedy_speedup = results[i][0] / results[i][2];

    char bfs_str[16], greedy_str[16];
    if (bfs_speedup > 9999)
      sprintf(bfs_str, ">9999x");
    else
      sprintf(bfs_str, "%.1fx", bfs_speedup);

    if (greedy_speedup > 9999)
      sprintf(greedy_str, ">9999x");
    else
      sprintf(greedy_str, "%.0fx", greedy_speedup);

    printf("    n=%6d: solve_bfs %s, solve_greedy %s\n", sizes[i], bfs_str,
           greedy_str);
  }

  // =========================================================================
  // Benchmark 2: Fixed n=100000, varying s (max step size)
  // =========================================================================
  printf("\n");
  printf("  +-----------------------------------------------------------+\n");
  printf("  |     BENCHMARK 2: Fixed n=100000, varying max step (s)    |\n");
  printf("  +-----------------------------------------------------------+\n");

  int n_fixed = 100000;
  int steps[] = {2, 5, 10, 50, 100};
  int num_steps = sizeof(steps) / sizeof(steps[0]);
  double results_step[5][3];

  print_header_step(col_width);

  for (int i = 0; i < num_steps; i++) {
    int s = steps[i];
    generate_board_with_step(board, n_fixed, s);

    // Verify correctness
    int r1 = solve_dp(board, n_fixed);
    int r2 = solve_bfs(board, n_fixed);
    int r3 = solve_greedy(board, n_fixed);

    if (r1 != r2 || r2 != r3) {
      printf("ERROR: Results differ! dp=%d, bfs=%d, greedy=%d\n", r1, r2, r3);
      continue;
    }

    double t1 = benchmark(solve_dp, board, n_fixed, runs);
    double t2 = benchmark(solve_bfs, board, n_fixed, runs);
    double t3 = benchmark(solve_greedy, board, n_fixed, runs);

    results_step[i][0] = t1;
    results_step[i][1] = t2;
    results_step[i][2] = t3;

    print_row_step(s, t1, t2, t3, col_width);
  }

  print_footer(col_width);

  // Speedup summary for step benchmark
  printf("\n  Speedup vs solve_dp (n=%d):\n", n_fixed);
  for (int i = 0; i < num_steps; i++) {
    double bfs_speedup = results_step[i][0] / results_step[i][1];
    double greedy_speedup = results_step[i][0] / results_step[i][2];

    char bfs_str[16], greedy_str[16];
    sprintf(bfs_str, "%.1fx", bfs_speedup);
    sprintf(greedy_str, "%.0fx", greedy_speedup);

    printf("    s=%5d: solve_bfs %s, solve_greedy %s\n", steps[i], bfs_str,
           greedy_str);
  }

  printf("\n");

  free(board);
#if PREALLOC_ARRAYS
  free(g_dp);
  free(g_dist);
  free(g_queue);
#endif
  return 0;
}
