def attribute_overlap_score(attrs_a: dict, attrs_b: dict) -> float:
    """
    Compute a simple overlap score between two attribute dictionaries.
    """
    if not attrs_a or not attrs_b:
        return 0.0
    keys = set(attrs_a.keys()).union(attrs_b.keys())
    if not keys:
        return 0.0
    matches = 0
    for key in keys:
        if key in attrs_a and key in attrs_b and attrs_a[key] == attrs_b[key]:
            matches += 1
    return matches / len(keys)