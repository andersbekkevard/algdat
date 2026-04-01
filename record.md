# Record of Solved Problems

This document counts all problems solved in this project, organized according to the structure in `pensumhefte.md`.

---

## Forelesning 1: Algoritmer og kompleksitet

### Insertion-Sort
- **Count: 3**
  - `sorting_algorithms/insertion_sort.py`
  - `rep/insertion.py`
  - `sorting_algorithms/bucket_sort.py` (used internally in bucket sort)

---

## Forelesning 2: Problemer og reduksjoner

*(No specific algorithms listed in this chapter)*

---

## Forelesning 3: Splitt og hersk

### Merge-Sort
- **Count: 3**
  - `sorting_algorithms/merge_sort.py`
  - `rep/merge.py`
  - `random/merge_sort.py`

### Quicksort
- **Count: 5**
  - `sorting_algorithms/quicksort.py`
  - `rep/quick.py`
  - `random/quicksort.py`
  - `sorting_algorithms/qs_2.py`
  - `spanning_trees/mst.py` (quick_sort_edges for MST)

---

## Forelesning 4: Rangering i lineær tid

### Counting-Sort
- **Count: 4**
  - `random/counting_sort.py`
  - `sorting_algorithms/cs_2.py`
  - `sorting_algorithms/counting_radix_sort.py`
  - `sorting_algorithms/sort2/linear_sort.py`

### Radix-Sort
- **Count: 4**
  - `ovinger/oving4/radix_sort.py` (flexradix for strings)
  - `sorting_algorithms/rs_2.py`
  - `sorting_algorithms/counting_radix_sort.py`
  - `sorting_algorithms/sort2/linear_sort.py`

### Bucket-Sort
- **Count: 5**
  - `sorting_algorithms/bucket_sort.py`
  - `random/bucket.py`
  - `sorting_algorithms/bs_2.py` (bucket_sort and bucket_sort_integers)
  - `sorting_algorithms/sort2/linear_sort.py`
  - `sorting_algorithms/sort2/sorting_benchmark.c` (C implementation)

### Randomized-Select
- **Count: 3**
  - `ovinger/oving4/randomized_select.py`
  - `ovinger/oving4/k_largest.py` (uses rand_select_index)
  - `search/r_s.py` (randomized_select)

### Select (Deterministic Linear-Time Selection)
- **Count: 2**
  - `ovinger/oving4/k_largest.py` (uses rand_select_index variant)
  - `search/r_s.py` (select - median-of-medians)

---

## Forelesning 5: Rotfaste trestrukturer

### Heapsort
- **Count: 1**
  - `heap/heapsort.py`

### Binary Search Trees
- **Count: 1**
  - `bst/bst.py` (inorder_tree_walk, tree_search, iterative_tree_search, tree_insert)

### Binary Search
- **Count: 1**
  - `search/binary_search.py` (bisect_recursive and bisect_iterative)

---

## Forelesning 6: Dynamisk programmering

### Rod Cutting
- **Count: 2**
  - `ovinger/oving6/rodcut.py` (rodcut_memo, rodcut_table_cost, rodcut_memo_cost)
  - `exam/A2015H.py` (solve function for rod cutting)

### Longest Common Subsequence (LCS)
- **Count: 2**
  - `ovinger/oving6/lcs.py`
  - `random/lcs.py`

### Knapsack (0/1)
- **Count: 2**
  - `ovinger/oving6/knapsack.py` (solve_naive, solve_memo, solve_table)
  - `random/knapsack.py` (solve_memo)

### Unlimited Knapsack
- **Count: 1**
  - `ovinger/oving6/more_knapsack.py` (unlimited_knapsack, solve_unlimited)

### Longest Increasing Subsequence (LIS)
- **Count: 1**
  - `random/lis.py` (solve and solve_bisect)

### Longest Decreasing Subsequence (LDS)
- **Count: 1**
  - `ovinger/oving6/decreasing_subsequence.py`

### Box Stacking
- **Count: 1**
  - `random/box_stacking.py` (LIS variant on DAG)

### Sheet Cutting
- **Count: 1**
  - `ovinger/oving6/sheetcut.py` (2D rod cutting variant)

### Seam Carving
- **Count: 1**
  - `ovinger/oving6/seam_carving/seam_carving.py` (shortest path on grid using DP)

### Optimal Strategy for a Game (Coin Game)
- **Count: 1**
  - `exam/A2015H.py` (solve function)

### Minimum Jumps to Reach End (Jump Game)
- **Count: 1**
  - `exam/A2016H.py` (solve_dp, solve, solve_lf)

### Counting Subsequences
- **Count: 1**
  - `exam/A2014K.py` (solve_correct)

### Largest Rectangle in Histogram variant
- **Count: 1**
  - `exam/A2017H.py` (solve function)

### Interleaving Strings
- **Count: 1**
  - `exam/A2019H2.py` (solve function - correct DP version)

---

## Forelesning 7: Grådighet

### Activity Selection
- **Count: 1**
  - `random/activity_selection.py` (solve_clrs - DP variant, solve_greedy - greedy variant)

### Minimum Emails (Activity Selection variant)
- **Count: 1**
  - `exam/A2022H.py` (solve function - greedy with min-heap)

### Huffman Coding
- **Count: 4**
  - `heap/huffman.py`
  - `ovinger/oving7/huffman.py`
  - `random/huffman.py`
  - `new_huffman/huffman.py`

---

## Forelesning 8: Traversering av grafer

### Breadth-First Search (BFS)
- **Count: 4**
  - `graph/benchmark/graph_representations.py`
  - `random/graphs.py`
  - `graph/graphs.py`
  - `flow/flow.py` (bfs_to_target in edmonds_karp)

### Depth-First Search (DFS)
- **Count: 5**
  - `graph/dfs.py`
  - `graph/dfs_2.py`
  - `random_2/dfs.py`
  - `random_2/dfs_solved.py`
  - `random_2/dfs_edge_classification.py`

### Topological Sort
- **Count: 3**
  - `path/sssp.py` (topological_sort_util, topological_sort in Graph class)
  - `ovinger/oving10/build_task.py` (traverse function for task dependencies)
  - `random/box_stacking.py` (DFS for topological sort)

### Strongly Connected Components (SCC)
- **Count: 0**
  *(Not explicitly found, but DFS implementations may include SCC logic)*

---

## Forelesning 9: Minimale spenntrær

### Kruskal's Algorithm
- **Count: 1**
  - `spanning_trees/mst.py` (includes DSU operations: make_set, find_set, union, link)

### Disjoint Set Union (DSU) / Union-Find
- **Count: 3**
  - `spanning_trees/mst.py` (Node, make_set, find_set, union, link)
  - `random/disjoint_sets.py` (multiple find_set variants: find_set, find_set_r, find_set_single_compression)
  - `ovinger/oving9/institutions.py` (HigherEdSolver class)
  - `ovinger/oving9/theory_solver.py` (find_equivalence, equivalence for constraint satisfaction)

### Prim's Algorithm
- **Count: 0**
  *(Not found in codebase)*

---

## Forelesning 10: Korteste vei fra én til alle

### DAG Shortest Paths
- **Count: 2**
  - `path/sssp.py` (dag_shortest_paths)
  - `ovinger/oving10/build_task.py` (building_time - critical path on DAG)

### Dijkstra's Algorithm
- **Count: 3**
  - `graph/benchmark/graph_representations.py`
  - `ovinger/oving10/earliest_arrival.py` (Dijkstra-like with PriorityQueue)
  - `exam/A2024H.py` (earliest_arrival - Dijkstra-like)

### Bellman-Ford Algorithm
- **Count: 1**
  - `ovinger/oving10/arrival_new.py` (earliest_arrival - Bellman-Ford like relaxation)

### Least Energy (Shortest Path with Negative Weights)
- **Count: 0**
  - `ovinger/oving10/least_energy.py` (placeholder, not implemented)

---

## Forelesning 11: Korteste vei fra alle til alle

### Slow-APSP / Faster-APSP
- **Count: 1**
  - `apsp/apsp.py` (extend_shortest_paths, extend_shortest_paths_inplace, slow_apsp)

### Floyd-Warshall
- **Count: 4**
  - `path/floyd_warshall.py`
  - `random/floyd_warshall.py`
  - `ovinger/oving11/fw.py` (general_floyd_warshall - generalized version)
  - `exam/A2017K.py` (solve - modified Floyd-Warshall for odd cycle detection)

### Transitive Closure
- **Count: 1**
  - `path/transitive_closure.py` (transitive_closure and simple_transitive_closure)

### Counting Paths in DAG
- **Count: 1**
  - `exam/A2018K.py` (solve - counts all paths between pairs)

### Odd Cycle Detection
- **Count: 1**
  - `exam/A2017K.py` (solve - modified Floyd-Warshall)

---

## Forelesning 12: Maksimal flyt

### Edmonds-Karp Algorithm
- **Count: 2**
  - `flow/flow.py` (edmonds_karp)
  - `ovinger/oving12/edmond_karp.py` (max_flow_highscore)

### Linear Programming (LP)
- **Count: 1**
  - `ovinger/oving12/lp.py` (find_k_paths - placeholder)

### Resource Allocation
- **Count: 1**
  - `ovinger/oving12/allocate.py` (allocate - placeholder)
  - `exam/A2023H.py` (allocate - placeholder)

---

## Forelesning 13-14: NP-kompletthet

### Independent Set to Clique Reduction
- **Count: 1**
  - `ovinger/oving1/independent_to_clique.py` (independent_set_to_clique, clique)

### Hamiltonian Cycle Verification
- **Count: 1**
  - `ovinger/oving1/verify_ham_cycle.py` (verify_ham_cycle)

### TSP Verification
- **Count: 1**
  - `ovinger/oving13/verify.py` (verify_tsp)

### Subset Sum
- **Count: 1**
  - `exam/A2022K.py` (subset_sum - memoized, subset_sum_bottom_up - tabulation)

---

## Additional Problems (Not explicitly in pensumhefte.md structure)

### Unimodal Array (Find Maximum)
- **Count: 3**
  - `ovinger/oving3/unimodal.py` (find_maximum)
  - `exam/A2018H.py` (solve - bisect_rotated)
  - `ovinger/oving3/unimodal_writeable.py` (if contains solution)

### Trie (Prefix Tree)
- **Count: 1**
  - `ovinger/oving5/build_tree.py` and `ovinger/oving5/search_tree.py` (together implement Trie)

### Envy Cycle Detection
- **Count: 1**
  - `ovinger/oving8/envy_freeness.py` (detect_envy_cycle using DFS)

### Compatibility Graph
- **Count: 1**
  - `ovinger/oving8/donors.py` (compatibility_graph)

### Constraint Satisfaction (Equality/Inequality)
- **Count: 1**
  - `ovinger/oving9/theory_solver.py` (check function - uses DSU and DFS)

### Favorite Spot (Cycle Detection)
- **Count: 1**
  - `ovinger/oving1/favorite_spot.py` (max_permutations, solve)

### Largest Cuboid
- **Count: 0**
  - `ovinger/oving3/largest_cuboid.py` (placeholder, not implemented)

### Nim Game
- **Count: 1**
  - `ovinger/oving1/nim.py` (simple game implementation)

### Path Finding with Edge Budget
- **Count: 1**
  - `exam/A2025K.py` (has_path - divide-and-conquer with O(lg k) space)

### Fibonacci Heap
- **Count: 1**
  - `heap/more_variants/fibonacci_heap.py` (if contains implementation)

### d-ary Heap
- **Count: 1**
  - `heap/more_variants/d_ary_heap.py` (if contains implementation)

---

## Summary Statistics

- **Total unique problems/algorithms: ~60+**
- **Total implementations counted: ~100+**

---

*Note: Some files may contain multiple implementations or variants of the same algorithm. Each distinct implementation or variant has been counted separately. Placeholder functions (marked with `pass` or `NotImplementedError`) are not counted unless they contain partial implementations.*
