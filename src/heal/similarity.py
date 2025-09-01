from typing import Dict, Optional

def attribute_overlap_score(a: Optional[Dict[str,str]], b: Optional[Dict[str,str]]) -> float:
    if not a or not b:
        return 0.0
    keys = set(a.keys()) | set(b.keys())
    if not keys:
        return 0.0
    hits = sum(1 for k in keys if k in a and k in b and a[k] == b[k])
    return hits / float(len(keys))
