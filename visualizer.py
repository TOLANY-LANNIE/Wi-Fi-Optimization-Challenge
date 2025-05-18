import matplotlib.pyplot as plt
import numpy as np
from interference_checker import get_interfering_pairs

"""
    Plot the number of interfering hotspots per iteration
     Args:
        interference_counts
    Returns:
"""
def plot_optimization_progress(interference_counts):
    plt.figure(figsize=(10, 6))
    plt.plot(interference_counts, 'b-o', linewidth=2)
    plt.xlabel('Optimization Iteration', fontsize=12)
    plt.ylabel('Number of Interfering Hotspots', fontsize=12)
    plt.title('Optimization Progress', fontsize=14)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('optimization_progress.png')
    plt.show()

"""
    Plot the hotspot locations with channel colors and interference indicators
    
    Args:
        hotspots
        interference_distances
    Returns:
"""
def plot_hotspot_map(hotspots, interference_distance=275):
    channel_colors = {1: 'blue', 2: 'green', 3: 'orange', 4: 'purple', 5: 'cyan'}

    # Get interfering pairs
    interfering_pairs = get_interfering_pairs(hotspots, interference_distance)

    # Get set of hotspots that are interfering
    interfering_hotspots = set(h for pair in interfering_pairs for h in pair)

    plt.figure(figsize=(12, 12))

    # Plot the hotspots
    for h in hotspots:
        border_color = 'red' if h in interfering_hotspots else 'black'
        plt.plot(h.x, h.y, 'o', color=channel_colors[h.channel],
                 markeredgecolor=border_color, markersize=8, markeredgewidth=1.5)

    # Plot the interference lines
    for h1, h2 in interfering_pairs:
        plt.plot([h1.x, h2.x], [h1.y, h2.y], 'r-', linewidth=0.5, alpha=0.3)

    # Add legend
    legend_elements = [plt.Line2D([0], [0], marker='o', color='w',
                                  markerfacecolor=channel_colors[i], markeredgecolor='black',
                                  markersize=8, label=f'Channel {i}')
                       for i in range(1, 6)]

    plt.legend(handles=legend_elements, loc='upper right')

    plt.xlim(0, 5000)
    plt.ylim(0, 5000)
    plt.xlabel('X coordinate (meters)', fontsize=12)
    plt.ylabel('Y coordinate (meters)', fontsize=12)
    plt.title(f'Wi-Fi Hotspot Map\n{len(interfering_hotspots)} interfering hotspots out of {len(hotspots)}',
              fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('hotspot_map.png')
    plt.show()