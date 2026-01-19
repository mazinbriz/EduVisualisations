# Physical Space Factors and Consequences
## Faculty of Education and MDAP quick consult 
### created 15 Jul 2025, last updated 15 Jul 2025

### Data collated by Sarah Temperley
### Visualisations by Amanda Belton

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import textwrap
import os

showNbrs = True

# Define the factors and their consequences with values
data = {
    "Physical space utilisation": {
        "Difficult to concentrate, focus, and work": 18,
        "Overwhelm, stress, sensory overload and negative emotions": 16,
        "Distracted": 15,
        "Hypervigilance and constant need to mask": 18,
        "Feeling marginalized and/or unaccommodated within the workplace": 12,
        "Physical pain or discomfort": 7,
        "Have to create own accommodations or do extra work to accommodate": 7,
        "Interrupted": 11,
        "Avoid or want to avoid the office": 11,
        "Have to choose between accommodating different needs": 4
    },
    "Noise": {
        "Difficult to concentrate, focus, and work": 12,
        "Overwhelm, stress, sensory overload and negative emotions": 13,
        "Distracted": 8,
        "Feeling marginalized and/or unaccommodated within the workplace": 5,
        "Physical pain or discomfort": 3,
        "Have to create own accommodations or do extra work to accommodate": 19,
        "Avoid or want to avoid the office": 7,
        "Have to choose between accommodating different needs": 5
    },
    "Lighting": {
        "Difficult to concentrate, focus, and work": 2,
        "Overwhelm, stress, sensory overload and negative emotions": 6,
        "Distracted": 1,
        "Feeling marginalized and/or unaccommodated within the workplace": 5,
        "Physical pain or discomfort": 8,
        "Avoid or want to avoid the office": 1
    },
    "Temperature": {
        "Difficult to concentrate, focus, and work": 5,
        "Overwhelm, stress, sensory overload and negative emotions": 1,
        "Physical pain or discomfort": 1,
        "Have to create own accommodations or do extra work to accommodate": 1
    },
    "Odour": {
        "Overwhelm, stress, sensory overload and negative emotions": 1,
        "Feeling marginalized and/or unaccommodated within the workplace": 1
    }
}

# colours from Sarah
Colours = {
    'Physical space utilisation': '#004949',
    'Have to choose between accommodating different needs' : '#009292',
    'Avoid or want to avoid the office' : '#FF6DB6',
    'Distracted': '#FFB6DB',
    'Temperature': '#490092',
    'Feeling marginalized and/or unaccommodated within the workplace': '#006DDB',
    'Physical pain or discomfort': '#B66DFF',
    'Have to create own accommodations or do extra work to accommodate': '#6DB6FF',
    'Interrupted': '#B6DBFF',
    'Overwhelm, stress, sensory overload and negative emotions': '#920000',
    'Difficult to concentrate, focus, and work': '#924900',
    'Noise': '#DB6D00',
    'Hypervigilance and constant need to mask' : '#24FF24',
    'Lighting': '#FFFF6D',
    'Odour': '#000000'
}

# Create the graph
G = nx.DiGraph()

# Calculate nbr participants for each factor and consequence
factor_totals = {factor: sum(consequences.values()) for factor, consequences in data.items()}
consequence_totals = {}
for consequences in data.values():
    for consequence, value in consequences.items():
        consequence_totals[consequence] = consequence_totals.get(consequence, 0) + value
# Calculate total number of participants
total_participants = sum(factor_totals.values())

# Add nodes and edges
for factor, consequences in data.items():
    G.add_node(factor, color=Colours.get(factor, '#000000'))
    for consequence in consequences:
        G.add_node(consequence, color=Colours.get(consequence, '#000000'))
        G.add_edge(factor, consequence)

node_colors = [Colours.get(node, '#000000') for node in G.nodes]

# Identify factors and consequences
factors = list(data.keys())
consequences = list(set(consequence for consequences in data.values() for consequence in consequences))

# Build edge colors based on the consequence (target node)
edge_colors = [Colours.get(tgt, '#000000') for src, tgt in G.edges()]

# Reverse the order of factors for plotting
factors = factors[::-1]

# Use bipartite layout: factors on the left (x=0), consequences on the right (x=1)
pos = {}
y_factors = np.linspace(0, 1, len(factors))
y_consequences = np.linspace(0, 1, len(consequences))
for i, node in enumerate(factors):
    pos[node] = (0, y_factors[i])
for i, node in enumerate(consequences):
    pos[node] = (1, y_consequences[i])

# create plot figure with title and headings
plottitle = "Physical Space Factors and Consequences"
fig, ax = plt.subplots(figsize=(12, 10))
plt.text(1.2, 1.075, "Consequences (number of participants)", 
         ha='center', va='bottom', fontsize=16, color='#000000')

# Draw edges
nx.draw_networkx_edges(G, pos, ax=ax, edge_color=edge_colors, width=2, alpha=0.5)

# Draw nodes
nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=3000, edgecolors= '#A9A9A9', linewidths=2)

# Add small circles around each factor
factor_size = 3000
small_circle_size = factor_size * 0.2
radius = 0.07
for factor in factors:
    fx, fy = pos[factor]
    linked_consequences = data[factor]
    n = len(linked_consequences)
    for j, (consequence, value) in enumerate(linked_consequences.items()):
        angle = 2 * np.pi * j / n
        cx = fx + radius * np.cos(angle)
        cy = fy + radius * np.sin(angle)
        color = Colours.get(consequence, '#888888')
        ax.scatter(cx, cy, s=small_circle_size, color=color, edgecolor='#A9A9A9', zorder=10)
        if showNbrs:
            # Add the value in the center of the circle
            ax.text(cx, cy, str(value), ha='center', va='center', fontsize=10, fontweight='bold', color='white', zorder=11)

# Manually add labels for each node
for node, (x, y) in pos.items():
    if node in factors:
        if node != 'Odour':
            ax.text(x - 0.08, y+.1, f"{node} ({factor_totals[node]})", ha='left', va='center', fontsize=14, fontweight='bold', color='#000000')
        else:
            ax.text(x - 0.05, y+.06, f"{node} ({factor_totals[node]})", ha='left', va='center', fontsize=14, fontweight='bold', color='#000000')
    else:
        wrapped_label = "\n".join(textwrap.wrap(f"{node} ({consequence_totals[node]})", width=25))
        ax.text(x + 0.06, y, wrapped_label, ha='left', va='center', fontsize=14, fontweight='bold', color='#000000')
            
        if False:
            # Show raw value (not %) for each consequence
            rawvalue = consequence_totals[node]
            percentage = (consequence_totals[node] / total_participants) * 100 # show piechart proportion from percentage  
            
            ax.text(x, y + 0.02, f"{rawvalue:.1f}", ha='center', va='center', fontsize=10, fontweight='bold', color='white')
            
            # Add black triangle representing the percentage
            triangle_size = 0.05  # Keep this value as is for consistent size
            angle = (percentage / 100) * 2 * np.pi
            # Adjust the center of the triangle to be at the center of the node
            triangle_center_x = x
            triangle_center_y = y
            # adjust bottom of triangle for larger percentages
            adjFactor = 1 + percentage/140
            # Calculate triangle points
            triangle_x = [
                triangle_center_x,
                triangle_center_x + triangle_size * np.cos(angle/2 - np.pi/2),
                triangle_center_x + triangle_size * np.cos(-angle/2 - np.pi/2)
            ]
            triangle_y = [
                triangle_center_y - triangle_size * 0.1, # move the top point down to look like a pie chart
                triangle_center_y + triangle_size * np.sin(angle/2 - np.pi/2)*adjFactor,
                triangle_center_y + triangle_size * np.sin(-angle/2 - np.pi/2)*adjFactor
            ]
            triangle = plt.Polygon(list(zip(triangle_x, triangle_y)), facecolor='#A9A9A9', edgecolor='none', zorder=3)
            ax.add_patch(triangle)

#plt.title(plottitle, fontdict={'fontsize': 24}, loc='right')
plt.axis('off')
plt.tight_layout()

plt.subplots_adjust(right=.7)

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Create a subdirectory called 'outputs' if it doesn't exist
output_dir = os.path.join(script_dir, 'outputs')
os.makedirs(output_dir, exist_ok=True)

# Create the full path for the output file
output_file = os.path.join(output_dir, plottitle + " with Nbrs.png")

# Save the figure
plt.savefig(output_file, bbox_inches='tight', format="png")
print(f"Saved figure as {plottitle}.png")
plt.close()
#plt.show()


