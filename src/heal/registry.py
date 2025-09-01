import json, os, time
from typing import Dict
from .types import Registry, LocatorEntry

REG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "config", "locators.json")

class LocatorRegistry:
    def __init__(self) -> None:
        with open(os.path.abspath(REG_PATH), "r", encoding="utf-8") as f:
            data = json.load(f)
        self.reg: Registry = {}
        for k, v in data.items():
            entry = LocatorEntry(
                context=v.get("context"),
                strategies=v.get("strategies", []),
                lastKnownSignature=v.get("lastKnownSignature")
            )
            self.reg[k] = entry

    def get(self, element_id: str) -> LocatorEntry:
        if element_id not in self.reg:
            raise KeyError(f"Locator '{element_id}' not found")
        return self.reg[element_id]

    def propose_update(self, element_id: str, updated: Dict) -> None:
        out_dir = os.path.abspath(os.path.join(os.getcwd(), "artifacts", "heals"))
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, f"{element_id}.{int(time.time()*1000)}.patch.json")
        payload = {"id": element_id, "updated": updated}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
