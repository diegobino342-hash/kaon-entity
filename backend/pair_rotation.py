import time

class PairRotationManager:
    def __init__(self, pairs, interval_seconds=10):
        self.pairs = pairs
        self.interval = interval_seconds
        self.index = 0
        self.current_pair = None
        self.last_switch = 0

    def should_switch(self):
        return time.time() - self.last_switch >= self.interval

    def next_pair(self):
        self.current_pair = self.pairs[self.index]
        self.index = (self.index + 1) % len(self.pairs)
        self.last_switch = time.time()
        return self.current_pair
