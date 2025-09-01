import json
import os
import time
from typing import Dict, List

from .types import Strategy, LocatorEntry


class LocatorRegistry:
    """
    Reads locators from a JSON file and allows proposing updates when healing occurs.
    """

    def __init__(self, config_path: str = None) -> None:
        # Default to config/locators.json relative to project root
        default_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'locators.json')
        self.config_path = config_path or default_path
        self._registry: Dict[str, LocatorEntry] = {}
        self._load()

    def _load(self) -> None:
        with open(self.config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for element_id, entry in data.items():
            strategies = [Strategy(**s) for s in entry.get('strategies', [])]
            self._registry[element_id] = LocatorEntry(strategies=strategies)

    def get(self, element_id: str) -> LocatorEntry:
        if element_id not in self._registry:
            raise KeyError(f"Locator '{element_id}' not found")
        return self._registry[element_id]

    def propose_update(self, element_id: str, new_primary: Strategy) -> None:
        """Propose an update that promotes new_primary to the first position."""
        entry = self.get(element_id)
        # If the new primary is already first, do nothing
        if entry.strategies and entry.strategies[0].type == new_primary.type and entry.strategies[0].value == new_primary.value:
            return
        # Build updated list: start with new_primary then include all other strategies except duplicates
        updated_strategies: List[Dict] = [{'type': new_primary.type, 'value': new_primary.value}]
        for strat in entry.strategies:
            if strat.type == new_primary.type and strat.value == new_primary.value:
                continue
            updated_strategies.append({'type': strat.type, 'value': strat.value})
        # Write a patch file under artifacts/heals
        out_dir = os.path.join(os.getcwd(), 'artifacts', 'heals')
        os.makedirs(out_dir, exist_ok=True)
        patch = {
            'id': element_id,
            'updated': {
                'strategies': updated_strategies
            }
        }
        fname = f"{element_id}.{int(time.time())}.patch.json"
        patch_path = os.path.join(out_dir, fname)
        with open(patch_path, 'w', encoding='utf-8') as f:
            json.dump(patch, f, indent=2)
        # Also write to events log
        events_path = os.path.join(out_dir, 'events.jsonl')
        with open(events_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(patch) + "\n")