import random

import networkx as nx
import matplotlib.pyplot as plt

def generate_complete_graph(num_nodes, weight_range=(1, 100)):
    graph = nx.complete_graph(num_nodes)
    for u , v in graph.edges():
        graph.edges[u, v]['weights'] = random.randint(*weight_range)
    return graph

def plot_graph_step(graph, tour, curr, pos):
    plt.clf()
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=500)
    path_edges = list(zip(tour, tour[1:]))
    nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='red', width=2)
    nx.draw_networkx_nodes(graph, pos, nodelist=[curr], node_color='green')

    edge_labels = nx.get_edge_attributes(graph, name='weights')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

    plt.pause(0.5)


def calculate_tour_cost(graph, tour):
    return sum(graph[tour[i]][tour[i + 1]]['weights'] for i in range(len(tour) - 1))


def nearest_neighbor_tsp(graph, start_node=None):
    if start_node is None:
        start_node = random.choice(list(graph.nodes))

    pos = nx.spiral_layout(graph)
    plt.ion()
    plt.show()

    unvisited = set(graph.nodes)
    unvisited.remove(start_node)
    tour = [start_node]
    curr = start_node

    plot_graph_step(graph, tour, curr, pos)

    while unvisited:
        next_node = min(unvisited, key=lambda node: graph[curr][node]['weights'])
        unvisited.remove(next_node) 
        tour.append(next_node)
        curr = next_node
        plot_graph_step(graph, tour, curr, pos)

    tour.append(start_node)
    plot_graph_step(graph, tour, curr, pos)

    print(tour)
    tour_cost = calculate_tour_cost(graph, tour)
    print(f'Construction Heuristic Tour Cost: {tour_cost}')

    plt.ioff()
    plt.show()

if __name__ == '__main__':
    graph = generate_complete_graph(6)

    nearest_neighbor_tsp(graph, start_node=0)
