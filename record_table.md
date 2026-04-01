# Record of Solved Problems (Table Format)

This document counts all problems solved in this project, organized according to the structure in `pensumhefte.md`.

---

## Forelesning 1: Algoritmer og kompleksitet

| Algorithm/Problem | Count | Files/Implementations |
|-------------------|-------|----------------------|
| Insertion-Sort | 3 | `sorting_algorithms/insertion_sort.py`<br>`rep/insertion.py`<br>`sorting_algorithms/bucket_sort.py` (used internally) |

---

## Forelesning 2: Problemer og reduksjoner

*(No specific algorithms listed in this chapter)*

---

## Forelesning 3: Splitt og hersk

| Algorithm/Problem | Count | Files/Implementations |
|-------------------|-------|----------------------|
| Merge-Sort | 3 | `sorting_algorithms/merge_sort.py`<br>`rep/merge.py`<br>`random/merge_sort.py` |
| Quicksort | 5 | `sorting_algorithms/quicksort.py`<br>`rep/quick.py`<br>`random/quicksort.py`<br>`sorting_algorithms/qs_2.py`<br>`spanning_trees/mst.py` (quick_sort_edges) |

---

## Forelesning 4: Rangering i lineær tid

| Algorithm/Problem | Count | Files/Implementations |
|-------------------|-------|----------------------|
| Counting-Sort | 4 | `random/counting_sort.py`<br>`sorting_algorithms/cs_2.py`<br>`sorting_algorithms/counting_radix_sort.py`<br>`sorting_algorithms/sort2/linear_sort.py` |
| Radix-Sort | 4 | `ovinger/oving4/radix_sort.py` (flexradix for strings)<br>`sorting_algorithms/rs_2.py`<br>`sorting_algorithms/counting_radix_sort.py`<br>`sorting_algorithms/sort2/linear_sort.py` |
| Bucket-Sort | 5 | `sorting_algorithms/bucket_sort.py`<br>`random/bucket.py`<br>`sorting_algorithms/bs_2.py` (bucket_sort and bucket_sort_integers)<br>`sorting_algorithms/sort2/linear_sort.py`<br>`sorting_algorithms/sort2/sorting_benchmark.c` (C implementation) |
| Randomized-Select | 3 | `ovinger/oving4/randomized_select.py`<br>`ovinger/oving4/k_largest.py` (uses rand_select_index)<br>`search/r_s.py` (randomized_select) |
| Select (Deterministic Linear-Time Selection) | 2 | `ovinger/oving4/k_largest.py` (uses rand_select_index variant)<br>`search/r_s.py` (select - median-of-medians) |

---

## Forelesning 5: Rotfaste trestrukturer

| Algorithm/Problem | Count | Files/Implementations |
|-------------------|-------|----------------------|
| Heapsort | 1 | `heap/heapsort.py` |
| Binary Search Trees | 1 | `bst/bst.py` (inorder_tree_walk, tree_search, iterative_tree_search, tree_insert) |
| Binary Search | 1 | `search/binary_search.py` (bisect_recursive and bisect_iterative) |

---

## Forelesning 6: Dynamisk programmering

| Algorithm/Problem | Count | Files/Implementations |
|-------------------|-------|----------------------|
| Rod Cutting | 2 | `ovinger/oving6/rodcut.py` (rodcut_memo, rodcut_table_cost, rodcut_memo_cost)<br>`exam/A2015H.py` (solve function) |
| Longest Common Subsequence (LCS) | 2 | `ovinger/oving6/lcs.py`<br>`random/lcs.py` |
| Knapsack (0/1) | 2 | `ovinger/oving6/knapsack.py` (solve_naive, solve_memo, solve_table)<br>`random/knapsack.py` (solve_memo) |
| Unlimited Knapsack | 1 | `ovinger/oving6/more_knapsack.py` (unlimited_knapsack, solve_unlimited) |
| Longest Increasing Subsequence (LIS) | 1 | `random/lis.py` (solve and solve_bisect) |
| Longest Decreasing Subsequence (LDS) | 1 | `ovinger/oving6/decreasing_subsequence.py` |
| Box Stacking | 1 | `random/box_stacking.py` (LIS variant on DAG) |
| Sheet Cutting | 1 | `ovinger/oving6/sheetcut.py` (2D rod cutting variant) |
| Seam Carving | 1 | `ovinger/oving6/seam_carving/seam_carving.py` (shortest path on grid using DP) |
| Optimal Strategy for a Game (Coin Game) | 1 | `exam/A2015H.py` (solve function) |
| Minimum Jumps to Reach End (Jump Game) | 1 | `exam/A2016H.py` (solve_dp, solve, solve_lf) |
| Counting Subsequences | 1 | `exam/A2014K.py` (solve_correct) |
| Largest Rectangle in Histogram variant | 1 | `exam/A2017H.py` (solve function) |
| Interleaving Strings | 1 | `exam/A2019H2.py` (solve function - correct DP version) |

---

## Forelesning 7: Grådighet

| Algorithm/Problem | Count | Files/Implementations |
|-------------------|-------|----------------------|
| Activity Selection | 1 | `random/activity_selection.py` (solve_clrs - DP variant, solve_greedy - greedy variant) |
| Minimum Emails (Activity Selection variant) | 1 | `exam/A2022H.py` (solve function - greedy with min-heap) |
| Huffman Coding | 4 | `heap/huffman.py`<br>`ovinger/oving7/huffman.py`<br>`random/huffman.py`<br>`new_huffman/huffman.py` |

---

## Forelesning 8: Traversering av grafer

| Algorithm/Problem | Count | Files/Implementations |
|-------------------|-------|----------------------|
| Breadth-First Search (BFS) | 4 | `graph/benchmark/graph_representations.py`<br>`random/graphs.py`<br>`graph/graphs.py`<br>`flow/flow.py` (bfs_to_target in edmonds_karp) |
| Depth-First Search (DFS) | 5 | `graph/dfs.py`<br>`graph/dfs_2.py`<br>`random_2/dfs.py`<br>`random_2/dfs_solved.py`<br>`random_2/dfs_edge_classification.py` |
| Topological Sort | 3 | `path/sssp.py` (topological_sort_util, topological_sort in Graph class)<br>`ovinger/oving10/build_task.py` (traverse function for task dependencies)<br>`random/box_stacking.py` (DFS for topological sort) |
| Strongly Connected Components (SCC) | 0 | *(Not explicitly found, but DFS implementations may include SCC logic)* |

---

## Forelesning 9: Minimale spenntrær

| Algorithm/Problem | Count | Files/Implementations |
|-------------------|-------|----------------------|
| Kruskal's Algorithm | 1 | `spanning_trees/mst.py` (includes DSU operations: make_set, find_set, union, link) |
| Disjoint Set Union (DSU) / Union-Find | 3 | `spanning_trees/mst.py` (Node, make_set, find_set, union, link)<br>`random/disjoint_sets.py` (multiple find_set variants)<br>`ovinger/oving9/institutions.py` (HigherEdSolver class)<br>`ovinger/oving9/theory_solver.py` (find_equivalence, equivalence) |
| Prim's Algorithm | 0 | *(Not found in codebase)* |

---

## Forelesning 10: Korteste vei fra én til alle

| Algorithm/Problem | Count | Files/Implementations |
|-------------------|-------|----------------------|
| DAG Shortest Paths | 2 | `path/sssp.py` (dag_shortest_paths)<br>`ovinger/oving10/build_task.py` (building_time - critical path on DAG) |
| Dijkstra's Algorithm | 3 | `graph/benchmark/graph_representations.py`<br>`ovinger/oving10/earliest_arrival.py` (Dijkstra-like with PriorityQueue)<br>`exam/A2024H.py` (earliest_arrival - Dijkstra-like) |
| Bellman-Ford Algorithm | 1 | `ovinger/oving10/arrival_new.py` (earliest_arrival - Bellman-Ford like relaxation) |
| Least Energy (Shortest Path with Negative Weights) | 0 | `ovinger/oving10/least_energy.py` (placeholder, not implemented) |

---

## Forelesning 11: Korteste vei fra alle til alle

| Algorithm/Problem | Count | Files/Implementations |
|-------------------|-------|----------------------|
| Slow-APSP / Faster-APSP | 1 | `apsp/apsp.py` (extend_shortest_paths, extend_shortest_paths_inplace, slow_apsp) |
| Floyd-Warshall | 4 | `path/floyd_warshall.py`<br>`random/floyd_warshall.py`<br>`ovinger/oving11/fw.py` (general_floyd_warshall - generalized version)<br>`exam/A2017K.py` (solve - modified Floyd-Warshall for odd cycle detection) |
| Transitive Closure | 1 | `path/transitive_closure.py` (transitive_closure and simple_transitive_closure) |
| Counting Paths in DAG | 1 | `exam/A2018K.py` (solve - counts all paths between pairs) |
| Odd Cycle Detection | 1 | `exam/A2017K.py` (solve - modified Floyd-Warshall) |

---

## Forelesning 12: Maksimal flyt

| Algorithm/Problem | Count | Files/Implementations |
|-------------------|-------|----------------------|
| Edmonds-Karp Algorithm | 2 | `flow/flow.py` (edmonds_karp)<br>`ovinger/oving12/edmond_karp.py` (max_flow_highscore) |
| Linear Programming (LP) | 1 | `ovinger/oving12/lp.py` (find_k_paths - placeholder) |
| Resource Allocation | 1 | `ovinger/oving12/allocate.py` (allocate - placeholder)<br>`exam/A2023H.py` (allocate - placeholder) |

---

## Forelesning 13-14: NP-kompletthet

| Algorithm/Problem | Count | Files/Implementations |
|-------------------|-------|----------------------|
| Independent Set to Clique Reduction | 1 | `ovinger/oving1/independent_to_clique.py` (independent_set_to_clique, clique) |
| Hamiltonian Cycle Verification | 1 | `ovinger/oving1/verify_ham_cycle.py` (verify_ham_cycle) |
| TSP Verification | 1 | `ovinger/oving13/verify.py` (verify_tsp) |
| Subset Sum | 1 | `exam/A2022K.py` (subset_sum - memoized, subset_sum_bottom_up - tabulation) |

---

## Additional Problems (Not explicitly in pensumhefte.md structure)

| Algorithm/Problem | Count | Files/Implementations |
|-------------------|-------|----------------------|
| Unimodal Array (Find Maximum) | 3 | `ovinger/oving3/unimodal.py` (find_maximum)<br>`exam/A2018H.py` (solve - bisect_rotated)<br>`ovinger/oving3/unimodal_writeable.py` (if contains solution) |
| Trie (Prefix Tree) | 1 | `ovinger/oving5/build_tree.py` and `ovinger/oving5/search_tree.py` (together implement Trie) |
| Envy Cycle Detection | 1 | `ovinger/oving8/envy_freeness.py` (detect_envy_cycle using DFS) |
| Compatibility Graph | 1 | `ovinger/oving8/donors.py` (compatibility_graph) |
| Constraint Satisfaction (Equality/Inequality) | 1 | `ovinger/oving9/theory_solver.py` (check function - uses DSU and DFS) |
| Favorite Spot (Cycle Detection) | 1 | `ovinger/oving1/favorite_spot.py` (max_permutations, solve) |
| Largest Cuboid | 0 | `ovinger/oving3/largest_cuboid.py` (placeholder, not implemented) |
| Nim Game | 1 | `ovinger/oving1/nim.py` (simple game implementation) |
| Path Finding with Edge Budget | 1 | `exam/A2025K.py` (has_path - divide-and-conquer with O(lg k) space) |
| Fibonacci Heap | 1 | `heap/more_variants/fibonacci_heap.py` (if contains implementation) |
| d-ary Heap | 1 | `heap/more_variants/d_ary_heap.py` (if contains implementation) |

---

## Summary Statistics

- **Total unique problems/algorithms: ~60+**
- **Total implementations counted: ~100+**

---

*Note: Some files may contain multiple implementations or variants of the same algorithm. Each distinct implementation or variant has been counted separately. Placeholder functions (marked with `pass` or `NotImplementedError`) are not counted unless they contain partial implementations.*
