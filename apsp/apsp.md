# apsp


> Converted from PDF • 20 of 20 pages


---

## Page 1

23 All-Pairs Shortest Paths In this chapter, we turn to the problem of finding shortest paths between all pairs of vertices in a graph.

A classic application of this problem occurs in computing a table of distances between all pairs of cities for a road atlas.

Classic perhaps, but not a true application of finding shortest paths between all pairs of vertices.

After all, a road map modeled as a graph has one vertex for every road intersection and one edge wherever a road connects intersections.

A table of intercity distances in an atlas might include distances for 100 cities, but the United States has approximately 300,000 signal-controlled intersections 1 and many more uncontrolled intersections.

A legitimate application of all-pairs shortest paths is to determine the diameter of a network: the longest of all shortest paths.

If a directed graph models a communication network, with the weight of an edge indicating the time required for a message to traverse a communication link, then the diameter gives the longest possible transit time for a message in the network.

As in Chapter 22, the input is a weighted, directed graph G = ( V , E ) with a weight function w : E → ℝ that maps edges to real-valued weights.

Now the goal is to find, for every pair of vertices u, v ∈ V , a shortest (least-weight) path from u to v , where the weight of a path is the sum of the weights of its constituent edges.

For the all-pairs problem, the output typically takes a tabular form in which the entry in u ’s row and v ’s column is the weight of a shortest path from u to v .

---

## Page 2

You can solve an all-pairs shortest-paths problem by running a single-source shortest-paths algorithm | V | times, once with each vertex as the source.

If all edge weights are nonnegative, you can use Dijkstra’s algorithm.

If you implement the min-priority queue with a linear array, the running time is O ( V 3 + VE ) which is O ( V 3 ).

The binary min-heap implementation of the min-priority queue yields a running time of O ( V ( V + E ) lg V ).

If | E | = Ω( V ), the running time becomes O ( VE lg V ), which is faster than O ( V 3 ) if the graph is sparse.

Alternatively, you can implement the min-priority queue with a Fibonacci heap, yielding a running time of O ( V 2 lg V + VE ).

If the graph contains negative-weight edges, Dijkstra’s algorithm doesn’t work, but you can run the slower Bellman-Ford algorithm once from each vertex.

The resulting running time is O ( V 2 E ), which on a dense graph is O ( V 4 ).

This chapter shows how to guarantee a much better asymptotic running time.

It also investigates the relation of the all-pairs shortest-paths problem to matrix multiplication.

Unlike the single-source algorithms, which assume an adjacency-list representation of the graph, most of the algorithms in this chapter represent the graph by an adjacency matrix.

(Johnson’s algorithm for sparse graphs, in Section 23.3, uses adjacency lists.) For convenience, we assume that the vertices are numbered 1, 2, … , | V |, so that the input is an n × n matrix W = ( wij ) representing the edge weights of an n -vertex directed graph G = ( V , E ), where The graph may contain negative-weight edges, but we assume for the time being that the input graph contains no negative-weight cycles.

The tabular output of each of the all-pairs shortest-paths algorithms presented in this chapter is an n × n matrix.

The ( i , j ) entry of the output matrix contains δ ( i , j), the shortest-path weight from vertex i to vertex j , as in Chapter 22.

---

## Page 3

A full solution to the all-pairs shortest-paths problem includes not only the shortest-path weights but also a predecessor matrix Π = (π ij ), where π ij is NIL if either i = j or there is no path from i to j , and otherwise π ij is the predecessor of j on some shortest path from i .

Just as the predecessor subgraph G π from Chapter 22 is a shortest-paths tree for a given source vertex, the subgraph induced by the i th row of the Π matrix should be a shortest-paths tree with root i .

For each vertex i ∈ V , the predecessor subgraph of G for i is G π, i = ( V π, i , E π, i ), where V π, i = { j ∈ V : π ij ≠ NIL} ∪ { i }, E π, i = {(π ij , j ) : j ∈ V π, i − { i }}.

If G π, i is a shortest-paths tree, then PRINT-ALL-PAIRS-SHORTEST- PATH on the following page, which is a modified version of the PRINT-PATH procedure from Chapter 20, prints a shortest path from vertex i to vertex j .

In order to highlight the essential features of the all-pairs algorithms in this chapter, we won’t cover how to compute predecessor matrices and their properties as extensively as we dealt with predecessor subgraphs in Chapter 22.

Some of the exercises cover the basics.

PRINT-ALL-PAIRS-SHORTEST-PATH( Π , i , j ) 1 if i == j 2 print i 3 elseif π ij == NIL 4 print “no path from” i “to” j “exists” 5 else PRINT-ALL-PAIRS-SHORTEST-PATH( Π , i , π ij ) 6 print j Chapter outline Section 23.1 presents a dynamic-programming algorithm based on matrix multiplication to solve the all-pairs shortest-paths problem.

The technique of “repeated squaring” yields a running time of Θ ( V 3 lg V ).

---

## Page 4

Section 23.2 gives another dynamic-programming algorithm, the Floyd- Warshall algorithm, which runs in Θ ( V 3 ) time.

Section 23.2 also covers the problem of finding the transitive closure of a directed graph, which is related to the all-pairs shortest-paths problem.

Finally, Section 23.3 presents Johnson’s algorithm, which solves the all-pairs shortest-paths problem in O ( V 2 lg V + VE ) time and is a good choice for large, sparse graphs.

Before proceeding, we need to establish some conventions for adjacency-matrix representations.

First, we generally assume that the input graph G = ( V , E ) has n vertices, so that n = | V |.

Second, we use the convention of denoting matrices by uppercase letters, such as W , L , or D , and their individual elements by subscripted lowercase letters, such as w ij , l ij , or d ij .

Finally, some matrices have parenthesized superscripts, as in or , to indicate iterates.

23.1 Shortest paths and matrix multiplication This section presents a dynamic-programming algorithm for the all- pairs shortest-paths problem on a directed graph G = ( V , E ).

Each major loop of the dynamic program invokes an operation similar to matrix multiplication, so that the algorithm looks like repeated matrix multiplication.

We’ll start by developing a Θ ( V 4 )-time algorithm for the all-pairs shortest-paths problem, and then we’ll improve its running time to Θ ( V 3 lg V ).

Before proceeding, let’s briefly recap the steps given in Chapter 14 for developing a dynamic-programming algorithm: 1.

Characterize the structure of an optimal solution.

2.

Recursively define the value of an optimal solution.

3.

Compute the value of an optimal solution in a bottom-up fashion.

We reserve the fourth step—constructing an optimal solution from computed information—for the exercises.

---

## Page 5

The structure of a shortest path Let’s start by characterizing the structure of an optimal solution.

Lemma 22.1 tells us that all subpaths of a shortest path are shortest paths.

Consider a shortest path p from vertex i to vertex j , and suppose that p contains at most r edges.

Assuming that there are no negative- weight cycles, r is finite.

If i = j , then p has weight 0 and no edges.

If vertices i and j are distinct, then decompose path p into , where path p ′ now contains at most r − 1 edges.

Lemma 22.1 says that p ′ is a shortest path from i to k , and so δ ( i , j ) = δ ( i , k ) + w kj .

A recursive solution to the all-pairs shortest-paths problem Now, let be the minimum weight of any path from vertex i to vertex j that contains at most r edges.

When r = 0, there is a shortest path from i to j with no edges if and only if i = j , yielding For r ≥ 1, one way to achieve a minimum-weight path from i to j with at most r edges is by taking a path containing at most r − 1 edges, so that .

Another way is by taking a path of at most r − 1 edges from i to some vertex k and then taking the edge ( k , j ), so that .

Therefore, to examine paths from i to j consisting of at most r edges, try all possible predecessors k of j , giving the recursive definition The last equality follows from the observation that w jj = 0 for all j .

What are the actual shortest-path weights δ ( i , j )? If the graph contains no negative-weight cycles, then whenever δ ( i , j ) < ∞, there is a shortest path from vertex i to vertex j that is simple.

(A path p from i to j that is not simple contains a cycle.

Since each cycle’s weight is nonnegative, removing all cycles from the path leaves a simple path with weight no greater than p ’s weight.) Because any simple path contains at

---

## Page 6

most n − 1 edges, a path from vertex i to vertex j with more than n − 1 edges cannot have lower weight than a shortest path from i to j .

The actual shortest-path weights are therefore given by Computing the shortest-path weights bottom up Taking as input the matrix W = ( w ij ), let’s see how to compute a series of matrices L (0) , L (1) , … , L ( n −1) , where for r = 0, 1, … , n − 1.

The initial matrix is L (0) given by equation (23.2).

The final matrix L ( n −1) contains the actual shortest-path weights.

The heart of the algorithm is the procedure EXTEND-SHORTEST- PATHS, which implements equation (23.3) for all i and j .

The four inputs are the matrix L ( r −1) computed so far; the edge-weight matrix W ; the output matrix L ( r ) , which will hold the computed result and whose elements are all initialized to ∞ before invoking the procedure; and the number n of vertices.

The superscripts r and r − 1 help to make the correspondence of the pseudocode with equation (23.3) plain, but they play no actual role in the pseudocode.

The procedure extends the shortest paths computed so far by one more edge, producing the matrix L ( r ) of shortest-path weights from the matrix L ( r −1) computed so far.

Its running time is Θ ( n 3 ) due to the three nested for loops.

EXTEND-SHORTEST-PATHS( L ( r −1) , W , L ( r ) , n ) 1 // Assume that the elements of L ( r ) are initialized to ∞.

2 for i = 1 to n 3 for j = 1 to n 4 for k = 1 to n 5 Let’s now understand the relation of this computation to matrix multiplication.

Consider how to compute the matrix product C = A · B

---

## Page 7

of two n × n matrices A and B .

The straightforward method used by MATRIX-MULTIPLY on page 81 uses a triply nested loop to implement equation (4.1), which we repeat here for convenience: for i , j = 1, 2, … , n .

Now make the substitutions l ( r −1) → a , w → b , l ( r ) → c , min → +, + → .

in equation (23.3).

You get equation (23.5)! Making these changes to EXTEND-SHORTEST-PATHS, and also replacing ∞ (the identity for min) by 0 (the identity for +), yields the procedure MATRIX- MULTIPLY.

We can see that the procedure EXTEND-SHORTEST- PATHS( L ( r −1) , W , L ( r ) , n ) computes the matrix “product” L ( r ) = L ( r −1) .

W using this unusual definition of matrix multiplication.

2 Thus, we can solve the all-pairs shortest-paths problem by repeatedly multiplying matrices.

Each step extends the shortest-path weights computed so far by one more edge using EXTEND-SHORTEST- PATHS( L ( r −1) , W , L ( r ) , n ) to perform the matrix multiplication.

Starting with the matrix L (0) , we produce the following sequence of n − 1 matrices corresponding to powers of W : L (1) = L (0) · W = W 1 , L (2) = L (1) · W = W 2 , L (3) = L (2) · W = W 3 , ⋮ L ( n −1) = L ( n −2) · W = W n −1 .

---

## Page 8

At the end, the matrix L ( n −1) = W n −1 contains the shortest-path weights.

The procedure SLOW-APSP on the next page computes this sequence in Θ ( n 4 ) time.

The procedure takes the n × n matrices W and L (0) as inputs, along with n .

Figure 23.1 illustrates its operation.

The pseudocode uses two n × n matrices L and M to store powers of W , computing M = L · W on each iteration.

Line 2 initializes L = L (0) .

For each iteration r , line 4 initializes M = ∞, where ∞ in this context is a matrix of scalar ∞ values.

The r th iteration starts with the invariant L = L ( r −1) = W r −1 .

Line 6 computes M = L · W = L ( r −1) · W = W r −1 · W = W r = L ( r ) so that the invariant can be restored for the next iteration by line 7, which sets L = M .

At the end, the matrix L = L ( n −1) = W n −1 of shortest-path weights is returned.

The assignments to n × n matrices in lines 2, 4, and 7 implicitly run doubly nested loops that take Θ ( n 2 ) time for each assignment.

The n − 1 invocations of EXTEND- SHORTEST-PATHS, each of which takes Θ ( n 3 ) time, dominate the computation, yielding a total running time of Θ ( n 4 ).

Figure 23.1 A directed graph and the sequence of matrices L ( r ) computed by SLOW-APSP.

You might want to verify that L (5) , defined as L (4) · W , equals L (4) , and thus L ( r ) = L (4) for all r ≥ 4.

SLOW-APSP( W , L (0) , n ) 1 let L = ( lij ) and M = ( mij ) be new n × n matrices

---

## Page 9

2 L = L (0) 3 for r = 1 to n − 1 4 M = ∞ // initialize M 5 // Compute the matrix “product” M = L · W .

6 EXTEND-SHORTEST-PATHS( L , W , M , n ) 7 L = M 8 return L Improving the running time Bear in mind that the goal is not to compute all the L ( r ) matrices: only the matrix L ( n −1) matters.

Recall that in the absence of negative-weight cycles, equation (23.4) implies L ( r ) = L ( n −1) for all integers r ≥ n − 1.

Just as traditional matrix multiplication is associative, so is matrix multiplication defined by the EXTEND-SHORTEST-PATHS procedure (see Exercise 23.1-4).

In fact, we can compute L ( n −1) with only ⌈ lg( n – 1) ⌉ matrix products by using the technique of repeated squaring : Since 2 ⌈ lg( n – 1) ⌉ ≥ n – 1, the final product is .

The procedure FASTER-APSP implements this idea.

It takes just the n × n matrix W and the size n as inputs.

Each iteration of the while loop of lines 4–8 starts with the invariant L = W r , which it squares using EXTEND-SHORTEST-PATHS to obtain the matrix M = L 2 = ( W r ) 2 = W 2 r .

At the end of each iteration, the value of r doubles, and L for the next iteration becomes M , restoring the invariant.

Upon exiting the loop when r ≥ n − 1, the procedure returns L = W r = L ( r ) = L ( n −1) by equation (23.4).

As in SLOW-APSP, the assignments to n × n

---

## Page 10

matrices in lines 2, 5, and 8 implicitly run doubly nested loops, taking Θ ( n 2 ) time for each assignment.

FASTER-APSP( W , n ) 1 let L and M be new n × n matrices 2 L = W 3 r = 1 4 while r < n − 1 5 M = ∞ // initialize M 6 EXTEND-SHORTEST- PATHS( L , L , M , n ) // compute M = L 2 7 r = 2 r 8 L = M // ready for the next iteration 9 return L Because each of the ⌈ lg( n – 1) ⌉ matrix products takes Θ ( n 3 ) time, FASTER-APSP runs in Θ ( n 3 lg n ) time.

The code is tight, containing no elaborate data structures, and the constant hidden in the Θ -notation is therefore small.

Exercises 23.1-1 Run SLOW-APSP on the weighted, directed graph of Figure 23.2, showing the matrices that result for each iteration of the loop.

Then do the same for FASTER-APSP.

Figure 23.2 A weighted, directed graph for use in Exercises 23.1-1, 23.2-1, and 23.3-1.

---

## Page 11

23.1-2 Why is it convenient for both SLOW-APSP and FASTER-APSP that wii = 0 for i = 1, 2, … , n ? 23.1-3 What does the matrix used in the shortest-paths algorithms correspond to in regular matrix multiplication? 23.1-4 Show that matrix multiplication defined by EXTEND-SHORTEST- PATHS is associative.

23.1-5 Show how to express the single-source shortest-paths problem as a product of matrices and a vector.

Describe how evaluating this product corresponds to a Bellman-Ford-like algorithm (see Section 22.1).

23.1-6 Argue that we don’t need the matrix M in SLOW-APSP because by substituting L for M and leaving out the initialization of M , the code still works correctly.

( Hint: Relate line 5 of EXTEND-SHORTEST- PATHS to RELAX on page 610.) Do we need the matrix M in FASTER-APSP? 23.1-7 Suppose that you also want to compute the vertices on shortest paths in the algorithms of this section.

Show how to compute the predecessor matrix Π from the completed matrix L of shortest-path weights in O ( n 3 ) time.

23.1-8

---

## Page 12

You can also compute the vertices on shortest paths along with computing the shortest-path weights.

Define as the predecessor of vertex j on any minimum-weight path from vertex i to vertex j that contains at most r edges.

Modify the EXTEND-SHORTEST-PATHS and SLOW-APSP procedures to compute the matrices Π (1) , Π (2) , … , Π ( n −1) as they compute the matrices L (1) , L (2) , … , L ( n −1) .

23.1-9 Modify FASTER-APSP so that it can determine whether the graph contains a negative-weight cycle.

23.1-10 Give an efficient algorithm to find the length (number of edges) of a minimum-length negative-weight cycle in a graph.

23.2 The Floyd-Warshall algorithm Having already seen one dynamic-programming solution to the all-pairs shortest-paths problem, in this section we’ll see another: the Floyd- Warshall algorithm , which runs in Θ ( V 3 ) time.

As before, negative- weight edges may be present, but not negative-weight cycles.

As in Section 23.1, we develop the algorithm by following the dynamic- programming process.

After studying the resulting algorithm, we present a similar method for finding the transitive closure of a directed graph.

The structure of a shortest path In the Floyd-Warshall algorithm, we characterize the structure of a shortest path differently from how we characterized it in Section 23.1.

The Floyd-Warshall algorithm considers the intermediate vertices of a shortest path, where an intermediate vertex of a simple path p = 〈 v 1, v 2, … , vl 〉 is any vertex of p other than v 1 or vl , that is, any vertex in the set { v 2, v 3, … , vl −1}.

---

## Page 13

The Floyd-Warshall algorithm relies on the following observation.

Numbering the vertices of G by V = {1, 2, … , n }, take a subset {1, 2, … , k } of vertices for some 1 ≤ k ≤ n .

For any pair of vertices i , j ∈ V , consider all paths from i to j whose intermediate vertices are all drawn from {1, 2, … , k }, and let p be a minimum-weight path from among them.

(Path p is simple.) The Floyd-Warshall algorithm exploits a relationship between path p and shortest paths from i to j with all intermediate vertices in the set {1, 2, … , k − 1}.

The details of the relationship depend on whether k is an intermediate vertex of path p or not.

Figure 23.3 Optimal substructure used by the Floyd-Warshall algorithm.

Path p is a shortest path from vertex i to vertex j , and k is the highest-numbered intermediate vertex of p .

Path p 1 , the portion of path p from vertex i to vertex k , has all intermediate vertices in the set {1, 2, … , k − 1}.

The same holds for path p 2 from vertex k to vertex j .

If k is not an intermediate vertex of path p , then all intermediate vertices of path p belong to the set {1, 2, … , k − 1}.

Thus a shortest path from vertex i to vertex j with all intermediate vertices in the set {1, 2, … , k − 1} is also a shortest path from i to j with all intermediate vertices in the set {1, 2, … , k }.

If k is an intermediate vertex of path p , then decompose p into , as Figure 23.3 illustrates.

By Lemma 22.1, p 1 is a shortest path from i to k with all intermediate vertices in the set {1, 2, … , k }.

In fact, we can make a slightly stronger statement.

Because vertex k is not an intermediate vertex of path p 1 , all intermediate vertices of p 1 belong to the set {1, 2, … , k − 1}.

Therefore p 1 is a shortest path from i to k with all intermediate vertices in the set {1, 2, … , k − 1}.

Likewise, p 2 is a shortest path

---

## Page 14

from vertex k to vertex j with all intermediate vertices in the set {1, 2, … , k − 1}.

A recursive solution to the all-pairs shortest-paths problem The above observations suggest a recursive formulation of shortest-path estimates that differs from the one in Section 23.1.

Let be the weight of a shortest path from vertex i to vertex j for which all intermediate vertices belong to the set {1, 2, … , k }.

When k = 0, a path from vertex i to vertex j with no intermediate vertex numbered higher than 0 has no intermediate vertices at all.

Such a path has at most one edge, and hence .

Following the above discussion, define recursively by Because for any path, all intermediate vertices belong to the set {1, 2, … , n }, the matrix gives the final answer: for all i , j ∈ V .

Computing the shortest-path weights bottom up Based on recurrence (23.6), the bottom-up procedure FLOYD- WARSHALL computes the values in order of increasing values of k .

Its input is an n × n matrix W defined as in equation (23.1).

The procedure returns the matrix D ( n ) of shortest-path weights.

Figure 23.4 shows the matrices D ( k ) computed by the Floyd-Warshall algorithm for the graph in Figure 23.1.

FLOYD-WARSHALL( W , n ) 1 D (0) = W 2 for k = 1 to n 3 let be a new n × n matrix 4 for i = 1 to n 5 for j = 1 to n 6 7 return D ( n )

---

## Page 15

The running time of the Floyd-Warshall algorithm is determined by the triply nested for loops of lines 2–6.

Because each execution of line 6 takes O (1) time, the algorithm runs in Θ ( n 3 ) time.

As in the final algorithm in Section 23.1, the code is tight, with no elaborate data structures, and so the constant hidden in the Θ -notation is small.

Thus, the Floyd-Warshall algorithm is quite practical for even moderate-sized input graphs.

Constructing a shortest path There are a variety of different methods for constructing shortest paths in the Floyd-Warshall algorithm.

One way is to compute the matrix D of shortest-path weights and then construct the predecessor matrix Π from the D matrix.

Exercise 23.1-7 asks you to implement this method so that it runs in O ( n 3 ) time.

Given the predecessor matrix Π , the PRINT-ALL-PAIRS-SHORTEST-PATH procedure prints the vertices on a given shortest path.

Alternatively, the predecessor matrix … can be computed while the algorithm computes the matrices D (0) , D (1) , … , D ( n ) .

Specifically, compute a sequence of matrices Π (0) , Π (1) , … , Π ( n ) , where Π = Π ( n ) and is the predecessor of vertex j on a shortest path from vertex i with all intermediate vertices in the set {1, 2, … , k }.

---

## Page 16

Figure 23.4 The sequence of matrices D ( k ) and Π ( k ) computed by the Floyd-Warshall algorithm for the graph in Figure 23.1.

Here’s a recursive formulation of .

When k = 0, a shortest path from i to j has no intermediate vertices at all, and so For k ≥ 1, if the path has k as an intermediate vertex, so that it is i ⇝ k ⇝ j where k ≠ j , then choose as the predecessor of j on this path the same vertex as the predecessor of j chosen on a shortest path from k with all intermediate vertices in the set {1, 2, … , k − 1}.

Otherwise, when the path from i to j does not have k as an intermediate vertex,

---

## Page 17

choose the same predecessor of j as on a shortest path from i with all intermediate vertices in the set {1, 2, … , k − 1}.

Formally, for k ≥ 1, Exercise 23.2-3 asks you to show how to incorporate the Π ( k ) matrix computations into the FLOYD-WARSHALL procedure.

Figure 23.4 shows the sequence of Π ( k ) matrices that the resulting algorithm computes for the graph of Figure 23.1.

The exercise also asks for the more difficult task of proving that the predecessor subgraph G π, i is a shortest-paths tree with root i .

Exercise 23.2-7 asks for yet another way to reconstruct shortest paths.

Transitive closure of a directed graph Given a directed graph G = ( V , E ) with vertex set V = {1, 2, … , n }, you might wish to determine simply whether G contains a path from i to j for all vertex pairs i , j ∈ V , without regard to edge weights.

We define the transitive closure of G as the graph G * = ( V , E *), where E * = {( i , j ) : there is a path from vertex i to vertex j in G }.

One way to compute the transitive closure of a graph in Θ ( n 3 ) time is to assign a weight of 1 to each edge of E and run the Floyd-Warshall algorithm.

If there is a path from vertex i to vertex j , you get dij < n .

Otherwise, you get d ij = ∞.

There is another, similar way to compute the transitive closure of G in Θ ( n 3 ) time, which can save time and space in practice.

This method substitutes the logical operations ∨ (logical OR) and ∧ (logical AND) for the arithmetic operations min and + in the Floyd-Warshall algorithm.

For i , j , k = 1, 2, … , n , define to be 1 if there exists a path in graph G from vertex i to vertex j with all intermediate vertices in the set {1, 2, … , k }, and 0 otherwise.

To construct the transitive closure G *

---

## Page 18

= ( V , E *), put edge ( i , j ) into E * if and only if .

A recursive definition of , analogous to recurrence (23.6), is Figure 23.5 A directed graph and the matrices T ( k ) computed by the transitive-closure algorithm.

and for k ≥ 1, As in the Floyd-Warshall algorithm, the TRANSITIVE-CLOSURE procedure computes the matrices in order of increasing k .

TRANSITIVE-CLOSURE( G , n ) 1 let be a new n × n matrix 2 for i = 1 to n 3 for j = 1 to n 4 if i == j or ( i , j ) ∈ G.E 5 6 else 7 for k = 1 to n 8 let be a new n × n matrix 9 for i = 1 to n 10 for j = 1 to n 11 12 return T ( n )

---

## Page 19

Figure 23.5 shows the matrices T ( k ) computed by the TRANSITIVE-CLOSURE procedure on a sample graph.

The TRANSITIVE-CLOSURE procedure, like the Floyd-Warshall algorithm, runs in Θ ( n 3 ) time.

On some computers, though, logical operations on single-bit values execute faster than arithmetic operations on integer words of data.

Moreover, because the direct transitive-closure algorithm uses only boolean values rather than integer values, its space requirement is less than the Floyd-Warshall algorithm’s by a factor corresponding to the size of a word of computer storage.

Exercises 23.2-1 Run the Floyd-Warshall algorithm on the weighted, directed graph of Figure 23.2.

Show the matrix D ( k ) that results for each iteration of the outer loop.

23.2-2 Show how to compute the transitive closure using the technique of Section 23.1.

23.2-3 Modify the FLOYD-WARSHALL procedure to compute the Π ( k ) matrices according to equations (23.7) and (23.8).

Prove rigorously that for all i ∈ V , the predecessor subgraph G π, i is a shortest-paths tree with root i .

( Hint: To show that G π, i is acyclic, first show that implies , according to the definition of .

Then adapt the proof of Lemma 22.16.) 23.2-4 As it appears on page 657, the Floyd-Warshall algorithm requires Θ ( n 3 ) space, since it creates for i , j , k = 1, 2, … , n .

Show that the procedure

---

## Page 20

FLOYD-WARSHALL ′ , which simply drops all the superscripts, is correct, and thus only Θ ( n 2 ) space is required.

FLOYD-WARSHALL ′ ( W , n ) 1 D = W 2 for k = 1 to n 3 for i = 1 to n 4 for j = 1 to n 5 d ij = min { d ij , d ik + d kj } 6 return D 23.2-5 Consider the following change to how equation (23.8) handles equality: Is this alternative definition of the predecessor matrix Π correct? 23.2-6 Show how to use the output of the Floyd-Warshall algorithm to detect the presence of a negative-weight cycle.

23.2-7 Another way to reconstruct shortest paths in the Floyd-Warshall algorithm uses values for i , j , k = 1, 2, … , n , where is the highest- numbered intermediate vertex of a shortest path from i to j in which all intermediate vertices lie in the set {1, 2, … , k }.

Give a recursive formulation for , modify the FLOYD-WARSHALL procedure to compute the values, and rewrite the PRINT-ALL-PAIRS- SHORTEST-PATH procedure to take the matrix as an input.

How is the matrix Φ like the s table in the matrix-chain multiplication problem of Section 14.2? 23.2-8