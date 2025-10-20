# src/atracer/log.py
import csv, os
class CSVLogger:
    def __init__(self, path):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self._header_written = os.path.exists(path)
    def log(self, **kw):
        with open(self.path, "a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=sorted(kw.keys()))
            if not self._header_written:
                w.writeheader()
                self._header_written = True
            w.writerow(kw)
