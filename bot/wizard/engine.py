from __future__ import annotations
from typing import Optional, Dict, Any, Tuple

from wizard.queue import (
    SmartQueue,
    QueueError,
    InvalidNavigationError,
    BranchConfigError,
)
from wizard.step import Step
from locales import translate as t
from core.logger import log


class WizardEngine:
    """
    High-level dialog controller.
    Handles errors, navigation, answer processing and logging.
    """

    def __init__(
        self,
        *,
        country: str,
        lang: str,
        base_steps: list[Step],
        debug: bool = False
    ):
        self.country = country
        self.lang = lang
        self.debug = debug

        try:
            self.queue = SmartQueue(base_steps, country=country)
        except Exception as e:
            log.error(f"[Wizard] Fatal init error: {e}", exc_info=True)
            raise

        if self.debug:
            log.info(f"[Wizard] Initialized (country={country}, lang={lang})")

        print("STEPS INIT:", len(self.queue.steps), [s.key for s in self.queue.steps])

    # -------------------------------------------------------------
    # 🟦 CURRENT STEP
    # -------------------------------------------------------------
    def current_step(self) -> Optional[Step]:
        try:
            step = self.queue.current()
            if self.debug:
                log.debug(f"[Wizard] current_step → {step.key if step else None}")
            return step
        except QueueError as e:
            log.error(f"[Wizard] current_step ERROR: {e}")
            return None

    # -------------------------------------------------------------
    # 🟩 NEXT STEP
    # -------------------------------------------------------------
    def next_step(self) -> Tuple[bool, Optional[Step], str]:
        """
        Returns:
            (success, step, message)
        """
        try:
            step = self.queue.next()
            if self.debug:
                log.debug(f"[Wizard] next_step → {step.key if step else None}")
            return True, step, "ok"

        except InvalidNavigationError as e:
            log.warning(f"[Wizard] Invalid next navigation: {e}")
            return False, None, "navigation_error"

        except QueueError as e:
            log.error(f"[Wizard] next_step queue error: {e}")
            return False, None, "queue_error"

        except Exception as e:
            log.error(f"[Wizard] next_step unexpected error: {e}", exc_info=True)
            return False, None, "fatal_error"

    # -------------------------------------------------------------
    # 🟥 PREVIOUS STEP
    # -------------------------------------------------------------
    def prev_step(self) -> Tuple[bool, Optional[Step], str]:
        try:
            step = self.queue.previous()
            if self.debug:
                log.debug(f"[Wizard] prev_step → {step.key if step else None}")
            return True, step, "ok"

        except InvalidNavigationError as e:
            log.warning(f"[Wizard] Invalid previous navigation: {e}")
            return False, None, "navigation_error"

        except QueueError as e:
            log.error(f"[Wizard] prev_step queue error: {e}")
            return False, None, "queue_error"

        except Exception as e:
            log.error(f"[Wizard] prev_step unexpected error: {e}", exc_info=True)
            return False, None, "fatal_error"

    # -------------------------------------------------------------
    # 📝 PROCESS ANSWER
    # -------------------------------------------------------------
    def process_answer(self, key: str, raw_value: str, display_value: str) -> Tuple[bool, str]:
        """
        Returns:
            (success, message)
        messages:
            - "ok"
            - "invalid"
            - "branch_error"
            - "queue_error"
            - "fatal_error"
        """
        print(len(self.queue.steps))
        if self.debug:
            log.debug(f"[Wizard] process_answer {key} = {raw_value}")

        try:
            normalized = self._normalize_answer(raw_value)

            self.queue.set_answer(key, normalized, display_value)

            return True, "ok"

        except BranchConfigError as e:
            log.error(f"[Wizard] BRANCH CONFIG ERROR for key='{key}': {e}")
            return False, "branch_error"

        except QueueError as e:
            log.error(f"[Wizard] QueueError while setting answer '{key}': {e}")
            return False, "queue_error"

        except Exception as e:
            log.error(f"[Wizard] Unexpected error in process_answer: {e}", exc_info=True)
            return False, "fatal_error"

    # -------------------------------------------------------------
    # 🔧 Normalize answer
    # -------------------------------------------------------------
    def _normalize_answer(self, answer: str) -> Any:
        try:
            local_yes = t(self.lang, "common.yes").lower()
            local_no = t(self.lang, "common.no").lower()

            a = answer.lower().strip()

            if a == local_yes:
                return "Yes"
            if a == local_no:
                return "No"

            return answer

        except Exception as e:
            log.error(f"[Wizard] normalize_answer error: {e}")
            return answer

    # -------------------------------------------------------------
    # 🔚 Finished?
    # -------------------------------------------------------------
    def is_finished(self) -> bool:
        return self.queue.is_finished()

    # -------------------------------------------------------------
    # 🧪 DEBUG DUMP
    # -------------------------------------------------------------
    def debug(self) -> Dict[str, Any]:
        try:
            return self.queue.debug_dump()
        except Exception as e:
            log.error(f"[Wizard] debug() error: {e}")
            return {}
