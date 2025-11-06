import networkx as nx
import random
import string
from typing import List, Dict, Tuple
from scipy.stats import spearmanr

def compute_ranking(graph: nx.DiGraph) -> List[Tuple[str, float]]:
    total_losses: Dict[str, float] = {}
    for _, v, data in graph.edges(data=True):
        total_losses[v] = total_losses.get(v, 0) + data['weight']

    epsilon = 1e-10

    node_ranking: List[Tuple[str, float]] = []
    for node in graph.nodes():
        score = 0
        for neighbor, edge_data in graph[node].items():
            score += edge_data['weight'] * (1 / (total_losses.get(neighbor, 0) + epsilon))
        node_ranking.append((node, score))

    node_ranking.sort(key=lambda x: x[1], reverse=True)
    return node_ranking

def generate_random_edges(players, min_weight=1, max_weight=20, seed=None) -> List[tuple[str, str, float]]:
    if seed is not None:
        random.seed(seed)

    edges = []
    for i in range(len(players)):
        for j in range(len(players)):
            if i != j:
                if random.choice([True, False]):
                    weight = random.randint(min_weight, max_weight)
                    edges.append((players[i], players[j], weight))
    return edges

def create_directed_weighted_graph(edges=None) -> nx.DiGraph:
    G = nx.DiGraph()
    if edges is not None:
        G.add_weighted_edges_from(edges)

    return G

if __name__ == "__main__":
    players: List[str] = list(string.ascii_uppercase)
    
    edges: List[Tuple[str, str, float]] = generate_random_edges(players, min_weight=0, max_weight=20)
    G: nx.DiGraph = create_directed_weighted_graph(edges)
    
    custom_node_ranking: List[Tuple[str, float]] = compute_ranking(G)
    
    hubs, authorities = nx.hits(G, max_iter=100, tol=1e-08)
    hubs_ranking = sorted(hubs.items(), key=lambda x: x[1], reverse=True)

    print("Rank | Your Ranking  | HITS Hub Score")
    print("---------------------------------------")
    for i in range(len(players)):
        print(f"{i+1:<4} | {custom_node_ranking[i][0]}: {custom_node_ranking[i][1]:.3f}   | {hubs_ranking[i][0]}: {hubs_ranking[i][1]:.3f}")

    print("\n" + "="*30)
    print("Ranking Similarity Analysis")
    print("="*30)

    custom_node_ranking_scores = dict(custom_node_ranking)
    my_aligned_scores = [custom_node_ranking_scores[player] for player in players]
    hits_aligned_scores = [hubs[player] for player in players]
    correlation, p_value = spearmanr(my_aligned_scores, hits_aligned_scores)

    print(f"Spearman's Rank Correlation: {correlation:.4f}")
    
    if correlation > 0.9:
        print("Result: The rankings are EXTREMELY similar.")
    elif correlation > 0.7:
        print("Result: The rankings are VERY similar.")
    elif correlation > 0.5:
        print("Result: The rankings are MODERATELY similar.")
    else:
        print("Result: The rankings are not very similar.")