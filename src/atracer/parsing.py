import re
from typing import Optional, Tuple

ANS_RE = re.compile(r"<answer>\s*([^|<>]+?)\s*\|\s*(\d+)\s*</answer>", re.IGNORECASE)

def extract_answer(text: str) -> Optional[Tuple[str, int]]:
    m = ANS_RE.search(text)
    if not m:
        return None
    agent = m.group(1).strip()
    step = int(m.group(2))
    return agent, step
