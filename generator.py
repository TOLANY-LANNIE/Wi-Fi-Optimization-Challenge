import random
import math
from hotspot import Hotspot

"""
    Calculate distance between two points
    Args:
        hotspot1 => x1,y1
        hotspot2 => x2,y2
    Returns:
        distance
"""
def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

"""
    Fun* generates random hotspots within a 5x5km area with minimum distance constraints
    Args:
        count
        min_distance
        area_size
    Returns:
        List of Hotspot objects
"""
def generate_hotspots(count=1000, min_distance=50, area_size=5000):
    hotspots = []
    attempts = 0
    max_attempts = 10000  # Safety valve

    while len(hotspots) < count and attempts < max_attempts:
        attempts += 1

        x = random.uniform(0, area_size)
        y = random.uniform(0, area_size)
        channel = random.randint(1, 5)

        # Check if this location is valid (at least min_distance from all existing hotspots)
        valid_location = True
        for h in hotspots:
            if distance(x, y, h.x, h.y) < min_distance:
                valid_location = False
                break
        # If it's a valid location then add the generated hotspot to the hotspots list
        if valid_location:
            hotspot_id = len(hotspots) + 1
            hotspots.append(Hotspot(hotspot_id, x, y, channel))

    print(f"Generated {len(hotspots)} hotspots after {attempts} attempts")
    return hotspots
