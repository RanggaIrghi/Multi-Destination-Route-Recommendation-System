import sys
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, ttk, Toplevel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def Multi_Destionation_Route(cost, selected_nodes):
    n = len(selected_nodes)
    dp = {}
    parent = {}

    def dynamic_programming(mask, pos):
        if mask == (1 << n) - 1:
            return cost[selected_nodes[pos]][selected_nodes[0]]
        
        if (mask, pos) in dp:
            return dp[(mask, pos)]
        
        ans = sys.maxsize
        best_next = None

        for i in range(n):
            if (mask & (1 << i)) == 0:
                new_mask = mask | (1 << i)
                temp_ans = cost[selected_nodes[pos]][selected_nodes[i]] + dynamic_programming(new_mask, i)
                
                if temp_ans < ans:
                    ans = temp_ans
                    best_next = i

        dp[(mask, pos)] = ans
        parent[(mask, pos)] = best_next
        return ans

    dynamic_programming(1, 0)
    
    path = [selected_nodes[0]]
    mask = 1
    curr = 0
    total_cost = 0

    while len(path) < n:
        next_node = parent.get((mask, curr), None)
        if next_node is None:
            break

        total_cost += cost[selected_nodes[curr]][selected_nodes[next_node]]
        path.append(selected_nodes[next_node])
        mask |= (1 << next_node)
        curr = next_node

    path.append(selected_nodes[0])
    total_cost += cost[selected_nodes[curr]][selected_nodes[0]]

    return path, total_cost

def visualize_graph(cost, path=None):
    G = nx.Graph()
    for i in cost.keys():
        for j in cost[i].keys():
            if i != j:
                G.add_edge(i, j, weight=cost[i][j])
    
    fig, ax = plt.subplots(figsize=(5, 4))
    pos = nx.circular_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', ax=ax, node_size=600)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)
    
    if path:
        edges_so_far = []
        for i in range(len(path) - 1):
            edges_so_far.append((path[i], path[i+1]))
            nx.draw_networkx_edges(G, pos, edgelist=edges_so_far, edge_color="red", width=2, ax=ax)
            nx.draw_networkx_nodes(G, pos, nodelist=[path[i]], node_color="green", ax=ax)
            plt.pause(0.7)
    
    return fig

def process_mdr():
    selected = entry_nodes.get().strip().split()
    selected = [node for node in selected if node in cost.keys()]
    
    if len(selected) < 2:
        messagebox.showwarning("Peringatan", "Masukkan minimal 2 node!")
        return
    
    path, total_cost = Multi_Destionation_Route(cost, selected)
    result_label.config(text=f'Jalur Optimal: \n{" → ".join(path)}\nTotal Biaya: {total_cost}', fg='white')
    
    new_window = Toplevel(root)
    new_window.title("Hasil")
    new_window.geometry("500x450")
    
    fig = visualize_graph(cost, path)
    canvas_result = FigureCanvasTkAgg(fig, master=new_window)
    canvas_result.get_tk_widget().pack()
    canvas_result.draw()

cost = {
    "A": {"A": 0, "B": 10, "C": 15, "D": 20, "E": 25},
    "B": {"A": 10, "B": 0, "C": 35, "D": 25, "E": 30},
    "C": {"A": 15, "B": 35, "C": 0, "D": 30, "E": 20},
    "D": {"A": 20, "B": 25, "C": 30, "D": 0, "E": 15},
    "E": {"A": 25, "B": 30, "C": 20, "D": 15, "E": 0},
}

root = tk.Tk()
root.title("Sistem Rekomendasi Rute Multi Tujuan")
root.geometry("800x400")

main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

left_frame = tk.Frame(main_frame)
left_frame.pack(side=tk.LEFT, padx=10, pady=10)

tk.Label(left_frame, text="Masukkan Node yang Ingin Dikunjungi (dipisah menggunakan spasi):").pack()
entry_nodes = tk.Entry(left_frame, width=30)
entry_nodes.pack()

tk.Button(left_frame, text="OK", command=process_mdr).pack(pady=10)
result_label = tk.Label(left_frame, text="", fg='white')
result_label.pack()

right_frame = tk.Frame(main_frame)
right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

fig = visualize_graph(cost)
canvas_map = FigureCanvasTkAgg(fig, master=right_frame)
canvas_map.get_tk_widget().pack()
canvas_map.draw()

root.mainloop()