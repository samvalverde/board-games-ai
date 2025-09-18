from dataclasses import dataclass
import time

@dataclass
class TimeMetric:
    elapsed_ms: float = 0.0
    _t0: float = 0.0
    def start(self):
        self._t0 = time.perf_counter()
        return self
    def stop(self):
        self.elapsed_ms = (time.perf_counter() - self._t0) * 1000.0
        return self
