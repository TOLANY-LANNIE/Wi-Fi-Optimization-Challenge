import random
from interference_checker import get_interfering_pairs, count_interferences_per_hotspot

"""
    Optimize channel assignment to minimize interference

    Args:
        hotspots: List of Hotspot objects
        max_iterations: Maximum number of optimization iterations
        interference_distance: Distance threshold for interference (in meters)
        stagnation_limit: Number of iterations with no improvement before applying randomization
        random_attempts: Number of random reassignments to try when stuck in local minimum

    Returns:
        Tuple of (hotspots with optimized channels, list of interference counts by iteration)
"""


def optimize_channels(hotspots, max_iterations=100, interference_distance=275, stagnation_limit=5, random_attempts=10):
    results = []

    # Get initial interference count
    current_interfering_pairs = get_interfering_pairs(hotspots, interference_distance)
    interfering_hotspots_count = len(set(h for pair in current_interfering_pairs for h in pair))
    results.append(interfering_hotspots_count)

    print(f"Starting optimization with {interfering_hotspots_count} interfering hotspots")

    iteration = 0
    stagnation_counter = 0

    while iteration < max_iterations:
        if len(current_interfering_pairs) == 0:
            print(f"Optimization complete: No interferences after {iteration} iterations")
            break

        # Get hotspots with interferences and their counts
        interference_counts = count_interferences_per_hotspot(hotspots, interference_distance)

        # Track current interference level before making changes
        current_interference_level = sum(interference_counts.values())

        if stagnation_counter >= stagnation_limit:
            # Apply randomization to escape local minimum
            print(f"Iteration {iteration + 1}: Local minimum detected, applying {random_attempts} random changes...")
            best_random_hotspots = None
            best_random_interference = current_interference_level

            # Try multiple random reassignments and keep the best one
            for _ in range(random_attempts):
                # Create a temporary copy of the current channel assignments
                temp_channels = {h.id: h.channel for h in hotspots}

                # Apply random changes to a subset of problematic hotspots
                problematic_hotspots = sorted(
                    [(h_id, count) for h_id, count in interference_counts.items() if count > 0],
                    key=lambda x: x[1],
                    reverse=True
                )[:max(3, len(interference_counts) // 5)]  # Focus on top ~20% worst offenders

                for h_id, _ in problematic_hotspots:
                    for h in hotspots:
                        if h.id == h_id:
                            # Choose a different channel
                            current_channel = h.channel
                            new_channel = random.choice([c for c in range(1, 6) if c != current_channel])
                            h.channel = new_channel
                            break

                # Evaluate this random assignment
                test_pairs = get_interfering_pairs(hotspots, interference_distance)
                test_interference_counts = count_interferences_per_hotspot(hotspots, interference_distance)
                test_interference_level = sum(test_interference_counts.values())

                # If better than our best random solution so far, remember it
                if test_interference_level < best_random_interference:
                    best_random_interference = test_interference_level
                    best_random_hotspots = {h.id: h.channel for h in hotspots}

                # Restore original channels for next attempt
                for h in hotspots:
                    h.channel = temp_channels[h.id]

            # Apply the best random solution if it's better than current
            if best_random_hotspots and best_random_interference < current_interference_level:
                for h in hotspots:
                    h.channel = best_random_hotspots[h.id]

                current_interfering_pairs = get_interfering_pairs(hotspots, interference_distance)
                interfering_hotspots_count = len(set(h for pair in current_interfering_pairs for h in pair))
                results.append(interfering_hotspots_count)

                print(
                    f"Iteration {iteration + 1}: Applied random changes, reduced interferences to {interfering_hotspots_count}")
                stagnation_counter = 0  # Reset stagnation counter
            else:
                print(f"Iteration {iteration + 1}: Random changes didn't help, continuing with greedy approach")
                results.append(results[-1])  # No improvement
                stagnation_counter += 1
        else:
            # Standard greedy optimization step
            # Find the hotspot with the most interferences
            worst_hotspots = sorted(
                [(h_id, count) for h_id, count in interference_counts.items()],
                key=lambda x: x[1],
                reverse=True
            )

            if not worst_hotspots:
                break

            improved = False

            # Try to improve each of the top interfering hotspots
            for worst_hotspot_id, interferences in worst_hotspots[:3]:  # Try top 3 worst offenders
                if interferences == 0:
                    continue  # Skip hotspots with no interferences

                # Find the actual hotspot object
                worst_hotspot = None
                for h in hotspots:
                    if h.id == worst_hotspot_id:
                        worst_hotspot = h
                        break

                if not worst_hotspot:
                    continue

                # Try all possible channels and pick the best one
                original_channel = worst_hotspot.channel
                best_channel = original_channel
                best_interference_level = current_interference_level

                for test_channel in range(1, 6):
                    if test_channel == original_channel:
                        continue

                    # Temporarily change channel
                    worst_hotspot.channel = test_channel

                    # Count interferences with this channel
                    test_interference_counts = count_interferences_per_hotspot(hotspots, interference_distance)
                    test_interference_level = sum(test_interference_counts.values())

                    # If this channel is better than our best so far, remember it
                    if test_interference_level < best_interference_level:
                        best_interference_level = test_interference_level
                        best_channel = test_channel

                # Restore original channel temporarily
                worst_hotspot.channel = original_channel

                # Apply the best channel if it reduces interference
                if best_channel != original_channel and best_interference_level < current_interference_level:
                    worst_hotspot.channel = best_channel
                    current_interfering_pairs = get_interfering_pairs(hotspots, interference_distance)
                    interfering_hotspots_count = len(set(h for pair in current_interfering_pairs for h in pair))

                    print(f"Iteration {iteration + 1}: Changed channel for hotspot {worst_hotspot.id} "
                          f"from {original_channel} to {best_channel}, interferences: {interfering_hotspots_count}")

                    improved = True
                    stagnation_counter = 0  # Reset stagnation counter
                    break  # Move to next iteration after successful improvement

            if improved:
                results.append(interfering_hotspots_count)
            else:
                print(f"Iteration {iteration + 1}: No improvement found")
                results.append(results[-1])  # No change in interference count
                stagnation_counter += 1

        iteration += 1

    # Final interference assessment
    final_interfering_pairs = get_interfering_pairs(hotspots, interference_distance)
    final_interference_count = len(set(h for pair in final_interfering_pairs for h in pair))

    print(f"Optimization completed after {iteration} iterations")
    print(f"Final interference count: {final_interference_count}")

    return hotspots, results