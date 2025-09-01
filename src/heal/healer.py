from __future__ import annotations
import json, os, time
from typing import Dict, List, Optional, Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from .registry import LocatorRegistry
from .similarity import attribute_overlap_score

def _to_by(strategy: Dict[str, object]):
    t = strategy["type"]
    v = strategy["value"]
    if t == "css":
        return (By.CSS_SELECTOR, v)
    if t == "xpath":
        return (By.XPATH, v)
    if t == "text":
        return (By.XPATH, f"//*[normalize-space(text())='{v}' or contains(normalize-space(.), '{v}')]")
    return (By.CSS_SELECTOR, v)

def _get_attrs(driver: WebDriver, el: WebElement) -> Dict[str,str]:
    try:
        attrs = driver.execute_script(
            "const e=arguments[0];const out={};for(const a of e.attributes){out[a.name]=a.value;}return out;", el)
        if isinstance(attrs, dict):
            return {str(k): str(v) for k, v in attrs.items()}
    except WebDriverException:
        pass
    return {}

class Healer:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.registry = LocatorRegistry()

    def _unique_or_none(self, by: str, value: str, context_css: Optional[str]) -> Optional[WebElement]:
        scope: Optional[WebElement] = None
        if context_css:
            scopes = self.driver.find_elements(By.CSS_SELECTOR, context_css)
            if len(scopes) != 1:
                return None
            scope = scopes[0]
        try:
            els = scope.find_elements(by, value) if scope else self.driver.find_elements(by, value)
        except Exception:
            return None
        return els[0] if len(els) == 1 else None

    def _score_candidate(self, el: WebElement, entry: Dict) -> float:
        last_sig = (entry.get("lastKnownSignature") or {})
        last_attrs = last_sig.get("attrs") or {}
        attrs = _get_attrs(self.driver, el)
        attr_score = attribute_overlap_score(last_attrs, attrs)
        visible = False; enabled = False
        try: visible = el.is_displayed()
        except Exception: pass
        try: enabled = el.is_enabled()
        except Exception: pass
        stable = (0.2 if visible else 0.0) + (0.1 if enabled else 0.0)
        return min(1.0, 0.7 * attr_score + stable)

    def find(self, element_id: str) -> WebElement:
        entry = self.registry.get(element_id)
        e_dict = {
            "context": entry.context,
            "strategies": entry.strategies,
            "lastKnownSignature": entry.lastKnownSignature
        }
        strategies: List[Dict] = sorted(e_dict["strategies"], key=lambda s: s.get("weight", 0), reverse=True)
        primary = strategies[0]
        by, val = _to_by(primary)
        fast = self._unique_or_none(by, val, e_dict["context"])
        if fast is not None:
            return fast

        best: Optional[Tuple[WebElement, Dict, float]] = None
        for s in strategies[1:]:
            by2, v2 = _to_by(s)
            el = self._unique_or_none(by2, v2, e_dict["context"])
            if el is None:
                continue
            score = self._score_candidate(el, e_dict)
            if best is None or score > best[2]:
                best = (el, s, score)

        if best and best[2] >= 0.75:
            self._report_heal(element_id, primary, best[1], best[2])
            updated = dict(e_dict)
            promoted = dict(best[1]); promoted["weight"] = 1.0
            updated["strategies"] = [promoted] + [s for s in e_dict["strategies"] if s is not best[1]]
            sig = { "tag": best[0].tag_name.lower(), "attrs": _get_attrs(self.driver, best[0]) }
            updated["lastKnownSignature"] = sig
            self.registry.propose_update(element_id, updated)
            return best[0]

        raise NoSuchElementException(f"Unable to locate '{element_id}' via self-healing")

    def _report_heal(self, element_id: str, old_primary: Dict, healed_with: Dict, score: float) -> None:
        out_dir = os.path.join(os.getcwd(), "artifacts", "heals")
        os.makedirs(out_dir, exist_ok=True)
        event = {
            "elementId": element_id,
            "oldPrimary": old_primary,
            "healedWith": healed_with | {"score": score},
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "pageUrl": self.driver.current_url,
            "score": score
        }
        print("[HEAL] " + json.dumps(event))
        with open(os.path.join(out_dir, "events.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")
