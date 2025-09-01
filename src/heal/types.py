from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Strategy:
    type: str
    value: str

@dataclass
class LocatorEntry:
    strategies: List[Strategy]

@dataclass
class RegistryPatch:
    id: str
    updated: Dict