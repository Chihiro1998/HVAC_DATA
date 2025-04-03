import pandas as pd
import plotly.graph_objects as go

# === Step 1: Load connection result CSV ===
df = pd.read_csv('../outputs/connection_mapping_analysis/final_connection_table.csv')

# === Step 2: Prepare node list ===
# Unique RTUs and VAVs
rtus = sorted(df['RTU'].unique().tolist())
vavs = sorted(df['VAV'].unique().tolist())

# All nodes (RTU first, then VAVs)
nodes = rtus + vavs
node_indices = {name: idx for idx, name in enumerate(nodes)}

# === Step 3: Prepare Sankey source & target indices ===
sources = [node_indices[row['RTU']] for _, row in df.iterrows()]
targets = [node_indices[row['VAV']] for _, row in df.iterrows()]
values = [1] * len(df)  # Each connection counts as 1

# === Step 4: Draw Sankey chart ===
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=nodes,
        color="lightblue"
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values,
        color="gray"
    ))])

fig.update_layout(title_text="RTU → VAV Connection Sankey Diagram", font_size=12)

# === Step 5: Save and show ===
fig.write_html("../outputs/connection_mapping_analysis/sankey_connection_graph.html")
print("Sankey diagram saved as sankey_connection_graph.html")
