#include <iostream>
#include <vector>
#include <chrono>
#include <iomanip>
#include <string>

struct Node {
    int value;
    Node* p;
    int rank;

    Node(int v) : value(v), p(this), rank(0) {}
};

Node* make_set(int value) {
    return new Node(value);
}

// Iterative find_set with full path compression
Node* find_set(Node* u) {
    Node* p = u->p;
    while (p != p->p) {
        p = p->p;
    }
    // Now p is the root - compress path
    Node* current = u;
    while (current->p != p) {
        Node* next = current->p;
        current->p = p;
        current = next;
    }
    return p;
}

// Recursive find_set with path compression
Node* find_set_r(Node* u) {
    if (u->p != u) {
        u->p = find_set_r(u->p);
    }
    return u->p;
}

void link(Node* u, Node* v) {
    if (u->rank >= v->rank) {
        v->p = u;
        u->rank = std::max(u->rank, v->rank + 1);
    } else {
        u->p = v;
        v->rank = std::max(v->rank, u->rank + 1);
    }
}

void union_sets(Node* u, Node* v) {
    link(find_set(u), find_set(v));
}

// Create a chain structure: 0 -> 1 -> 2 -> ... -> n-1 (n-1 is root)
std::vector<Node*> create_chain(int n) {
    std::vector<Node*> nodes;
    for (int i = 0; i < n; i++) {
        nodes.push_back(make_set(i));
    }
    for (int i = 0; i < n - 1; i++) {
        nodes[i]->p = nodes[i + 1];
    }
    nodes[n - 1]->p = nodes[n - 1]; // Root points to itself
    return nodes;
}

// Create a balanced tree structure
std::vector<Node*> create_tree(int n) {
    std::vector<Node*> nodes;
    for (int i = 0; i < n; i++) {
        nodes.push_back(make_set(i));
    }
    nodes[0]->p = nodes[0]; // Root points to itself
    for (int i = 1; i < n; i++) {
        int parent_idx = (i - 1) / 2;
        nodes[i]->p = nodes[parent_idx];
    }
    return nodes;
}

// Reset nodes to original structure
void reset_structure(std::vector<Node*>& nodes, const std::string& type) {
    int n = nodes.size();
    for (auto& node : nodes) {
        node->p = node;
        node->rank = 0;
    }

    if (type == "chain") {
        for (int i = 0; i < n - 1; i++) {
            nodes[i]->p = nodes[i + 1];
        }
        nodes[n - 1]->p = nodes[n - 1];
    } else if (type == "tree") {
        nodes[0]->p = nodes[0];
        for (int i = 1; i < n; i++) {
            int parent_idx = (i - 1) / 2;
            nodes[i]->p = nodes[parent_idx];
        }
    }
}

void cleanup(std::vector<Node*>& nodes) {
    for (auto& node : nodes) {
        delete node;
    }
    nodes.clear();
}

void print_separator(char c = '=', int width = 70) {
    std::cout << std::string(width, c) << "\n";
}

int main() {
    using namespace std::chrono;

    struct TestCase {
        std::string name;
        int n;
        std::string type;
    };

    std::vector<TestCase> test_cases = {
        {"Small chain (10 nodes)", 10, "chain"},
        {"Medium chain (100 nodes)", 100, "chain"},
        {"Large chain (1000 nodes)", 1000, "chain"},
        {"Small tree (100 nodes)", 100, "tree"},
        {"Medium tree (1000 nodes)", 1000, "tree"},
        {"Large tree (10000 nodes)", 10000, "tree"},
        {"XL tree (100000 nodes)", 100000, "tree"},
    };

    const int num_operations = 10000;

    print_separator();
    std::cout << "BENCHMARK: find_set (iterative) vs find_set_r (recursive)\n";
    print_separator();
    std::cout << "Operations per test: " << num_operations << " find operations\n\n";

    struct Result {
        std::string test;
        double iterative_ms;
        double recursive_ms;
        double speedup;
        std::string faster;
    };
    std::vector<Result> results;

    for (const auto& tc : test_cases) {
        std::cout << "Test: " << tc.name << "\n";
        print_separator('-');

        // Create structure
        std::vector<Node*> nodes;
        if (tc.type == "chain") {
            nodes = create_chain(tc.n);
        } else {
            nodes = create_tree(tc.n);
        }

        // Benchmark iterative version
        reset_structure(nodes, tc.type);
        auto start = high_resolution_clock::now();
        for (int i = 0; i < num_operations; i++) {
            find_set(nodes[0]);
        }
        auto end = high_resolution_clock::now();
        double iterative_ms = duration<double, std::milli>(end - start).count();

        // Benchmark recursive version
        reset_structure(nodes, tc.type);
        start = high_resolution_clock::now();
        for (int i = 0; i < num_operations; i++) {
            find_set_r(nodes[0]);
        }
        end = high_resolution_clock::now();
        double recursive_ms = duration<double, std::milli>(end - start).count();

        // Calculate speedup
        double speedup;
        std::string faster;
        if (iterative_ms < recursive_ms) {
            speedup = recursive_ms / iterative_ms;
            faster = "iterative";
        } else {
            speedup = iterative_ms / recursive_ms;
            faster = "recursive";
        }

        // Print results
        std::cout << std::fixed << std::setprecision(4);
        std::cout << "  Iterative (find_set):     " << std::setw(10) << iterative_ms << " ms\n";
        std::cout << "  Recursive (find_set_r):   " << std::setw(10) << recursive_ms << " ms\n";
        std::cout << std::setprecision(2);
        std::cout << "  Speedup:                  " << std::setw(10) << speedup << "x (" << faster << " is faster)\n\n";

        results.push_back({tc.name, iterative_ms, recursive_ms, speedup, faster});

        cleanup(nodes);
    }

    // Print summary
    print_separator();
    std::cout << "SUMMARY\n";
    print_separator();
    std::cout << std::left << std::setw(32) << "Test"
              << std::setw(12) << "Winner"
              << std::setw(10) << "Speedup" << "\n";
    print_separator('-');

    for (const auto& r : results) {
        std::cout << std::left << std::setw(32) << r.test
                  << std::setw(12) << r.faster
                  << std::fixed << std::setprecision(2) << r.speedup << "x\n";
    }
    std::cout << "\n";

    return 0;
}
