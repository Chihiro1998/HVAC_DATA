import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

# === Step 1: Load the final connection table ===
input_csv = '../outputs/connection_mapping_analysis/final_connection_table.csv'
df = pd.read_csv(input_csv)

# === Step 2: Create a directed graph ===
G = nx.DiGraph()

# Add nodes (RTUs and VAVs)
rtus = sorted(df['RTU'].unique().tolist())
vavs = sorted(df['VAV'].unique().tolist())

G.add_nodes_from(rtus, type='RTU')
G.add_nodes_from(vavs, type='VAV')

# Add edges from RTU → VAV
for _, row in df.iterrows():
    G.add_edge(row['RTU'], row['VAV'])

# === Step 3: Layout and drawing ===
pos = nx.spring_layout(G, k=0.7, seed=42)

# Color nodes
node_colors = []
for node in G.nodes():
    if G.nodes[node]['type'] == 'RTU':
        node_colors.append('skyblue')
    else:
        node_colors.append('lightgreen')

# Draw graph
plt.figure(figsize=(14, 10))
nx.draw(G, pos,
        with_labels=True,
        node_size=1000,
        node_color=node_colors,
        edge_color='gray',
        font_size=10,
        arrowsize=15)

plt.title('RTU–VAV Network Graph', fontsize=16)
plt.tight_layout()

# === Step 4: Save figure ===
output_path = '../outputs/connection_mapping_analysis/rtu_vav_network_graph.png'
plt.savefig(output_path)
plt.close()

print(f"Network graph saved to: {output_path}")
