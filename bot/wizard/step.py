from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Step:
    key: str
    countries: Optional[List[str]] = None
    is_quick: bool = False
    branch: Optional[str] = None
    validator: Optional[str] = None  # ← NEW FIELD

    def allowed(self, country: str) -> bool:
        if not self.countries:
            return True
        return "ALL" in self.countries or country in self.countries


__all__ = ["Step"]