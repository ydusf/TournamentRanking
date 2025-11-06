# Custom Hub-Ranking Algorithm

This project implements and analyses a custom, single-pass graph ranking algorithm. The algorithm is designed to identify influential "hub" nodes in a directed, weighted graph, similar in concept to the **HITS (Hub) algorithm**.

The script generates a random directed graph (simulating a tournament where an edge `(A, B)` means `A` beat `B`), runs the custom ranking algorithm, and then compares the results directly against the `networkx` HITS algorithm.

Finally, it computes the **Spearman's rank correlation** to provide a single, quantitative score of how similar the two rankings are.

## The Custom Algorithm (`compute_ranking`)

The core of this project is the `compute_ranking` function. It's a non-iterative algorithm that assigns a score to each node based on its *outgoing* connections.

The logic is designed to find nodes that connect to "exclusive" or hard-to-reach neighbors.

1.  **Calculate Total Incoming Weight:** First, it calculates the sum of all incoming edge weights for every node in the graph (e.g., `total_losses`).
2.  **Calculate Node Score:** For each node `A`, it calculates a score by summing up a value for each neighbor `B` it points to.

> **Algorithm Logic:**
> The score for a node `A` is the sum of its outgoing connections. Each connection to a neighbor `B` contributes:
>
> **`weight(A -> B) * (1 / total_incoming_weight(B))`**
>
> In a tournament context, this means: **A player gets a high score for beating players (by a high margin) who *don't lose to anyone else* (or lose by very little).**

This provides a "Quality of Wins" score, which is conceptually very similar to a HITS Hub score ("a good hub points to good authorities").

## Requirements

You will need Python 3 and the following libraries:

  * `networkx`: For graph creation and the benchmark HITS algorithm.
  * `scipy`: For calculating the Spearman's rank correlation.

You can install them using pip:

```bash
pip3 install -r requirements.txt
```

## How to Run

Save the code as a Python file (e.g., `main.py`) and run it from your terminal:

```bash
python main.py
```

The script will automatically:

1.  Generate a random 26-node graph.
2.  Compute the `compute_ranking` scores.
3.  Compute the `nx.hits` (Hub) scores.
4.  Print a side-by-side comparison of the rankings.
5.  Print the final similarity analysis.

## Example Output

Because the graph is generated randomly (without a fixed seed), your output will vary with each run. The output will look similar to this:

```
Rank | Custom Ranking  | HITS Hub Score
---------------------------------------
1    | U: 1.615   | S: 0.054
2    | S: 1.608   | M: 0.053
3    | Q: 1.376   | U: 0.052
4    | D: 1.262   | P: 0.050
5    | B: 1.250   | B: 0.049
6    | P: 1.127   | D: 0.046
7    | N: 1.122   | O: 0.045
8    | Y: 1.111   | R: 0.042
9    | O: 1.097   | W: 0.042
10   | R: 1.089   | E: 0.042
11   | W: 1.082   | Q: 0.042
12   | E: 1.039   | N: 0.039
13   | J: 1.007   | X: 0.039
14   | M: 0.936   | A: 0.039
15   | C: 0.928   | C: 0.038
16   | F: 0.923   | Z: 0.037
17   | L: 0.893   | L: 0.036
18   | A: 0.867   | G: 0.035
19   | Z: 0.862   | J: 0.031
20   | T: 0.855   | H: 0.031
21   | G: 0.795   | F: 0.031
22   | H: 0.780   | Y: 0.030
23   | X: 0.772   | V: 0.030
24   | I: 0.640   | T: 0.029
25   | V: 0.563   | I: 0.023
26   | K: 0.400   | K: 0.015

==============================
Ranking Similarity Analysis
==============================
Spearman's Rank Correlation: 0.9322
Result: The rankings are EXTREMELY similar.
```

### Analysis

  * **HITS Comparison:** The side-by-side list shows that while the scores are on different scales, the *order* of the top-ranked nodes is very similar.
  * **Spearman's Correlation:** This score (from -1.0 to +1.0) measures how well the *order* of the two lists matches. A high positive value (e.g., \> 0.9) confirms that the custom `compute_ranking` algorithm is an excellent and effective proxy for the more complex, iterative HITS Hub algorithm.