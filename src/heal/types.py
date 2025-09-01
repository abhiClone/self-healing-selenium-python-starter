from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Literal, Optional, TypedDict

StrategyType = Literal['css', 'xpath', 'text', 'ai']

@dataclass
class Strategy:
    type: StrategyType
    value: str
    weight: float  # 0..1

@dataclass
class Signature:
    tag: Optional[str] = None
    attrs: Dict[str, str] = field(default_factory=dict)

@dataclass
class LocatorEntry:
    context: Optional[str] = None   # CSS scoping root
    strategies: List[Strategy] = field(default_factory=list)
    lastKnownSignature: Optional[Signature] = None

Registry = Dict[str, LocatorEntry]

class HealEvent(TypedDict):
    elementId: str
    oldPrimary: Dict[str, object]
    healedWith: Dict[str, object]
    timestamp: str
    pageUrl: str
    score: float
