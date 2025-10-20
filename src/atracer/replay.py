# src/atracer/replay.py
import random
from collections import deque
from typing import Deque, Dict, Any, Iterable, List

class BalancedReplayBuffer:
    """Maintains 3 pools: clean, failing, and tracer-CF replays."""
    def __init__(self, cap_each: int = 2048):
        self.clean: Deque[Dict[str,Any]] = deque(maxlen=cap_each)
        self.fail:  Deque[Dict[str,Any]] = deque(maxlen=cap_each)
        self.cf:    Deque[Dict[str,Any]] = deque(maxlen=cap_each)

    def add(self, traj: Dict[str,Any]):
        if traj.get("cf_k") is not None:
            self.cf.append(traj)
        elif traj.get("passed", False):
            self.clean.append(traj)
        else:
            self.fail.append(traj)

    def sample(self, n:int, mix=(1,1,1)) -> List[Dict[str,Any]]:
        a,b,c = mix
        total = a+b+c
        n_clean = max(0, n * a // total)
        n_fail  = max(0, n * b // total)
        n_cf    = n - n_clean - n_fail
        out=[]
        def take(buf, k):
            src=list(buf)
            random.shuffle(src)
            out.extend(src[:k])
        take(self.clean, n_clean)
        take(self.fail,  n_fail)
        take(self.cf,    n_cf)
        random.shuffle(out)
        return out
