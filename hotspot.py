import math
"""
    Hotspot Class to create wifi hotspot objects
"""
class Hotspot:
    def __init__(self, id, x, y, channel):
        self.id = id
        self.x = x
        self.y = y
        self.channel = channel

    def __repr__(self):
        return f"Hotspot(id={self.id}, x={self.x:.1f}, y={self.y:.1f}, channel={self.channel})"
