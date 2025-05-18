from generator import generate_hotspots
from optimizer import optimize_channels
from visualizer import plot_optimization_progress, plot_hotspot_map
import pickle
import os

"""
    Save hotspots to a file
    Args:
        hotspots
        hotspots.pkl file
    Returns:
"""
def save_hotspots(hotspots, filename="hotspots.pkl"):
    with open(filename, 'wb') as f:
        pickle.dump(hotspots, f)
    print(f"Saved hotspots to {filename}")

"""
    Load hotspots from a file
    Args:
        hotspots.pkl file
    Returns:
        None
    
"""
def load_hotspots(filename="hotspots.pkl"):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            hotspots = pickle.load(f)
        print(f"Loaded {len(hotspots)} hotspots from {filename}")
        return hotspots
    return None


def main():
    # Part 1: Generate hotspots
    hotspots_file = "hotspots.pkl"

    # Try to load existing hotspots, or generate new ones
    hotspots = load_hotspots(hotspots_file)
    if not hotspots:
        hotspots = generate_hotspots(count=1000, min_distance=50, area_size=5000)
        save_hotspots(hotspots, hotspots_file)

    # Plot initial state
    plot_hotspot_map(hotspots)

    # Optimize channels
    optimized_hotspots, interference_history = optimize_channels(hotspots, max_iterations=50)

    # Plot optimization progress
    plot_optimization_progress(interference_history)

    # Plot final state
    plot_hotspot_map(optimized_hotspots)

    # Save optimized hotspots
    save_hotspots(optimized_hotspots, "optimized_hotspots.pkl")

if __name__ == "__main__":
    main()