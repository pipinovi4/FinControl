from __future__ import annotations
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

from wizard.step import Step
from config import BRANCH_MAP
from core import log


# ============================================================
# Exceptions (production-grade)
# ============================================================

class QueueError(Exception):
    """Base class for all SmartQueue-related errors."""


class StepNotFoundError(QueueError):
    """Raised when attempting to access a non-existing step index."""


class BranchConfigError(QueueError):
    """Raised when BRANCH_MAP is malformed or missing required fields."""


class InvalidNavigationError(QueueError):
    """Raised when navigation goes out of bounds."""


class DynamicInsertError(QueueError):
    """Raised when insertion or deletion of branch steps fails."""


# ============================================================
# SmartQueue — Dynamic Flow Engine
# ============================================================

@dataclass
class SmartQueue:
    """
    Dynamic smart queue for wizard-like questionnaire flow.
    """

    def __init__(self, steps: List[Step], *, country: str):
        self.country = country

        # Apply initial allowed() filters
        try:
            self.steps: List[Step] = [s for s in steps if s.allowed(country)]
            log.debug(f"[SmartQueue] Initialized with {len(self.steps)} steps for country={country}")
        except Exception as e:
            log.error(f"[SmartQueue] Initialization failed for country={country}: {e}")
            raise QueueError(f"Failed to initialize steps for country='{country}'") from e

        self.index: int = 0
        self.answers: Dict[str, Any] = {}
        self._inserted_by_parent: Dict[str, List[str]] = {}

    # ---------------------------------------------------------
    # ⏩ NAVIGATION
    # ---------------------------------------------------------

    def current(self) -> Optional[Step]:
        try:
            if self.index < 0:
                log.error(f"[SmartQueue] Negative index={self.index}")
                raise InvalidNavigationError(f"Negative index: {self.index}")

            if self.index >= len(self.steps):
                log.debug(f"[SmartQueue] current(): index out of range ({self.index})")
                return None

            return self.steps[self.index]

        except Exception as e:
            log.error(f"[SmartQueue] Failed to get current step at index={self.index}: {e}")
            raise QueueError(f"Failed to get current step at index={self.index}") from e

    def has_next(self) -> bool:
        return self.index + 1 < len(self.steps)

    def next(self) -> Optional[Step]:
        try:
            if self.index >= len(self.steps):
                log.warning("[SmartQueue] next(): Already at end of the queue")
                raise InvalidNavigationError("Already at the end of step list.")

            self.index += 1

            log.debug(f"[SmartQueue] Moved next → index={self.index}")

            if self.index >= len(self.steps):
                return None

            return self.steps[self.index]

        except Exception as e:
            log.error(f"[SmartQueue] Error during next() navigation: {e}")
            raise QueueError(f"Error during next() navigation, index={self.index}") from e

    def previous(self) -> Optional[Step]:
        try:
            if self.index == 0:
                log.warning("[SmartQueue] previous(): Already at the first step")
                raise InvalidNavigationError("Already at the first step.")

            self.index -= 1
            log.debug(f"[SmartQueue] Moved previous → index={self.index}")

            return self.steps[self.index]

        except Exception as e:
            log.error(f"[SmartQueue] Error during previous() navigation: {e}")
            raise QueueError(f"Error during previous() navigation, index={self.index}") from e

    # ---------------------------------------------------------
    # 📝 ANSWERS + BRANCHING
    # ---------------------------------------------------------

    def set_answer(self, key: str, canonical_value: Any, display_value: Any):
        """
        Stores dual-value answer + applies branching logic.
        """

        # Store both canonical + display
        self.answers[key] = {
            "canonical": canonical_value,
            "display": display_value,
        }

        log.debug(f"[SmartQueue] Answer saved: {key} = {self.answers[key]}")

        # Remove previous dynamic blocks
        self._remove_branch_for_parent(key)

        # Apply branching
        self._apply_branching(key, canonical_value)

    # ---------------------------------------------------------
    # 🔀 UNIVERSAL BRANCH ENGINE
    # ---------------------------------------------------------

    def _apply_branching(self, key: str, value: Any):
        try:
            cfg = BRANCH_MAP.get(key)
            if not cfg:
                log.debug(f"[SmartQueue] No branching for key='{key}'")
                return

            if "rules" not in cfg:
                raise BranchConfigError(f"Missing 'rules' in BRANCH_MAP for '{key}'")

            branch_type = cfg.get("type")
            rules = cfg["rules"]

            step_keys: List[str] = []

            if branch_type == "enum":
                step_keys = rules.get(value, [])

            elif branch_type == "yes_no":
                if value == "Yes":
                    step_keys = rules.get("Yes", [])

            else:
                raise BranchConfigError(f"Invalid branch type '{branch_type}' for '{key}'")

            if step_keys:
                log.info(f"[SmartQueue] Branch triggered for '{key}' → inserting {step_keys}")
                self._insert_steps(key, step_keys)
            else:
                log.debug(f"[SmartQueue] No dynamic steps for '{key}' and value='{value}'")

        except BranchConfigError:
            raise
        except Exception as e:
            log.error(f"[SmartQueue] Branching failed at key='{key}': {e}")
            raise QueueError(f"Branching failed for key='{key}', value='{value}'") from e

    # ---------------------------------------------------------
    # ➕ INSERT dynamic steps
    # ---------------------------------------------------------

    def _insert_steps(self, parent_key: str, step_keys: List[str]):
        try:
            insert_at = self.index + 1
            inserted = []

            for sk in reversed(step_keys):
                step = Step(key=sk, branch=parent_key)
                self.steps.insert(insert_at, step)
                inserted.append(sk)

            self._inserted_by_parent[parent_key] = inserted
            log.debug(f"[SmartQueue] Inserted dynamic steps after '{parent_key}': {inserted}")

        except Exception as e:
            log.error(f"[SmartQueue] Dynamic insertion failed for parent='{parent_key}': {e}")
            raise DynamicInsertError(
                f"Failed to dynamically insert steps for parent='{parent_key}'"
            ) from e

    # ---------------------------------------------------------
    # ❌ REMOVE dynamic branch steps
    # ---------------------------------------------------------

    def _remove_branch_for_parent(self, parent_key: str):
        try:
            if parent_key not in self._inserted_by_parent:
                return

            to_remove = set(self._inserted_by_parent[parent_key])

            log.info(f"[SmartQueue] Removing previously inserted steps for '{parent_key}': {to_remove}")

            self.steps = [s for s in self.steps if s.key not in to_remove]
            del self._inserted_by_parent[parent_key]

            # Fix index
            if self.index >= len(self.steps):
                self.index = max(0, len(self.steps) - 1)

        except Exception as e:
            log.error(f"[SmartQueue] Failed to remove dynamic steps for '{parent_key}': {e}")
            raise DynamicInsertError(
                f"Failed to remove dynamic steps for parent='{parent_key}'"
            ) from e

    # ---------------------------------------------------------
    # ✔ HELPERS
    # ---------------------------------------------------------

    def is_finished(self) -> bool:
        return self.index >= len(self.steps)

    def debug_dump(self):
        dump = {
            "country": self.country,
            "index": self.index,
            "current": self.current().key if self.current() else None,
            "steps": [s.key for s in self.steps],
            "answers": self.answers,
            "inserted": self._inserted_by_parent,
        }
        log.debug(f"[SmartQueue] Debug dump: {dump}")
        return dump
