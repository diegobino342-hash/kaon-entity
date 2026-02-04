import time

class CandleClock:
    def __init__(self, timeframe_seconds=300):
        self.tf = timeframe_seconds

    def current_bucket(self):
        now = int(time.time())
        return now - (now % self.tf)

    def seconds_to_close(self):
        now = int(time.time())
        return self.tf - (now % self.tf)
