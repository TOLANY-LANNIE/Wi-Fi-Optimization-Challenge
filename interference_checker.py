import math

"""
    Fun* finds all pairs of hotspots that interfere with each other
    Args:
        hotspots
        interference_distance
    Returns:
        List of tuples (hotspot1, hotspot2) that interfere with each other
"""
def get_interfering_pairs(hotspots, interference_distance=275):
    interfering_pairs = []

    for i, h1 in enumerate(hotspots):
        for j, h2 in enumerate(hotspots[i + 1:], i + 1):
            if h1.channel == h2.channel:
                d = distance(h1.x, h1.y, h2.x, h2.y)
                if d < interference_distance:
                    interfering_pairs.append((h1, h2))

    return interfering_pairs

"""
    Fun* calculates distance between two points
    Arg:
        hotspot1 x1 & y1 coordinates
        hotspot2 x2 & y2 coordinates
    Returns:
        distance
"""
def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

"""
    Count how many interferences each hotspot has
    Args:
        hotspots list
        interference_distance
    Returns:
        Dictionary with hotspot id as key and number of interferences as value
"""
def count_interferences_per_hotspot(hotspots, interference_distance=275):
    interferences = {h.id: 0 for h in hotspots}

    for i, h1 in enumerate(hotspots):
        for j, h2 in enumerate(hotspots):
            if i != j and h1.channel == h2.channel:
                d = distance(h1.x, h1.y, h2.x, h2.y)
                if d < interference_distance:
                    interferences[h1.id] += 1

    return interferences