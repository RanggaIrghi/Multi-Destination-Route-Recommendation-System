import sys
import networkx as nx
import matplotlib.pyplot as plt

def tsp(cost, selected_nodes):
    n = len(selected_nodes)

    dp = {}
    parent = {}

    def dpTSP(mask, pos):
        if mask == (1 << n) - 1:
            return cost[selected_nodes[pos]][selected_nodes[0]]
        
        if(mask, pos) in dp:
            return dp[(mask, pos)]
        
        ans = sys.maxsize
        best_next = None

        for i in range(n):
            if(mask & (1 << i)) == 0:
                new_mask = mask | (1 << i)
                temp_ans = cost[selected_nodes[pos]][selected_nodes[i]] + dpTSP(new_mask, i)

                if(temp_ans < ans):
                    ans = temp_ans
                    best_next = i

        dp[(mask, pos)] = ans
        parent[(mask, pos)] = best_next
        return ans

    dpTSP(1, 0)

    path = [selected_nodes[0]]
    mask = 1
    curr = 0
    total_cost = 0

    while len(path) < n:
        next_node = parent.get((mask, curr), None)
        if next_node is None:
            break

        total_cost+= cost[selected_nodes[curr]][selected_nodes[next_node]]
        path.append(selected_nodes[next_node])
        mask |= (1 << next_node)
        curr = next_node

    path.append(selected_nodes[0])
    total_cost += cost[selected_nodes[curr]][selected_nodes[0]]

    return path, total_cost

def generate_visualize_tsp(cost, path):
    G = nx.Graph()

    for i in cost.keys():
        for j in cost[i].keys():
            if i != j:
                G.add_edge(i, j, weight=cost[i][j])

    pos = nx.circular_layout(G)

    plt.ion()
    plt.figure(figsize=(8, 8))

    for i in range(len(path) - 1):
        plt.clf()

        nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=1000)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        edges_so_far = list(zip(path[: i + 1], path[1: i + 2]))
        nx.draw_networkx_edges(G, pos, edgelist=edges_so_far, edge_color="red", width=2)
        nx.draw_networkx_nodes(G, pos, nodelist=[path[i]], node_color="green")

        plt.pause(0.7)

    plt.ioff()
    plt.show()

if __name__ == "__main__":
    cost = {
        "A": {"A": 0, "B": 10, "C": 15, "D": 20, "E": 25},
        "B": {"A": 10, "B": 0, "C": 35, "D": 25, "E": 30},
        "C": {"A": 15, "B": 35, "C": 0, "D": 30, "E": 20},
        "D": {"A": 20, "B": 25, "C": 30, "D": 0, "E": 15},
        "E": {"A": 25, "B": 30, "C": 20, "D": 15, "E": 0},
    }
    
    selected_nodes = ["A", "E", "B", "C"]

    path, total_cost = tsp(cost, selected_nodes)
    print('')
    print("Node Yang Ingin Di kunjungi: ", selected_nodes)
    print("Jalur Optimal: ", path)
    print("Total Biaya: ", total_cost)
    print('')

    generate_visualize_tsp(cost, path)