from __future__ import annotations
from typing import Optional, Dict, Any, Tuple, Coroutine

from wizard.queue import (
    SmartQueue,
    QueueError,
    InvalidNavigationError,
    BranchConfigError,
)
from wizard.step import Step
from locales import translate as t, L10N
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
            if isinstance(raw_value, dict):
                normalized = raw_value
            else:
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

    async def validate_input(self, step_key: str, raw_value: str) -> tuple[bool, str, Any | None] | tuple[
        bool, str, str] | tuple[bool, str, str | Any] | tuple[bool, dict, str] | tuple[bool, Any, Any]:
        """
        Universal input validator.

        Returns:
            (ok: bool, canonical: str, display: str_or_error)
        """
        locale = L10N.get(self.lang, {})
        steps = locale.get("steps", {})
        by_country = locale.get("steps_by_country", {}).get(self.country, {})
        cfg = by_country.get(step_key, {}) or steps.get(step_key, {})

        validator_key = cfg.get("validator")

        # FILE UPLOAD → skip normalize
        if isinstance(raw_value, dict):
            # load validator
            from services.validators import VALIDATOR_REGISTRY
            validator = VALIDATOR_REGISTRY.get(validator_key)

            if not validator:
                # accept file without validation
                return True, raw_value, raw_value.get("name", "Документ")

            ok, result = await validator(raw_value)

            if not ok:
                return False, "", cfg.get("validator_error") or result

            # validator returns file_id → but we keep full dict
            canonical = raw_value
            display = raw_value.get("name", "Документ")
            return True, canonical, display

        # 1) Normalize yes/no (local language → Yes/No)
        raw_norm = self._normalize_answer(raw_value)

        # 2) Load config (steps + country overrides)
        validator_error_text = cfg.get("validator_error")

        # Quick buttons for this step
        quick = cfg.get("quick") or []

        # 3) 🔥 Convert BUTTON TEXT → KEY
        raw_norm = self._resolve_button_key(raw_norm, quick)

        # 4) If no validator → accept any value
        if not validator_key:
            canonical = raw_norm
            display = raw_norm

            # convert display via quick
            for btn in quick:
                if btn.get("key") == canonical:
                    display = btn.get("text", canonical)
                    break

            return True, canonical, display

        # 5) Load validator function
        from services.validators import VALIDATOR_REGISTRY
        validator = VALIDATOR_REGISTRY.get(validator_key)

        if not validator:
            return False, "", f"Missing validator '{validator_key}'"

        # 6) Special case: ENUM needs allowed list
        if validator_key == "enum":
            allowed = [btn.get("key") for btn in quick]
            try:
                ok, result = await validator(raw_norm, allowed)
            except Exception as e:
                log.error(f"[Wizard] Validator enum failed for {step_key}: {e}", exc_info=True)
                return False, "", "Ошибка валидации"
        else:
            # all other validators take (value)
            try:
                ok, result = await validator(raw_norm)
            except Exception as e:
                log.error(f"[Wizard] Validator failed for {step_key}: {e}", exc_info=True)
                return False, "", "Ошибка валидации"

        # 7) Validation failed → return error message
        if not ok:
            return False, "", validator_error_text or result

        # 8) SUCCESS — canonical = validator result
        canonical = result

        # convert display via quick buttons
        display = canonical
        for btn in quick:
            if btn.get("key") == canonical:
                display = btn.get("text", canonical)
                break

        return True, canonical, display

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

    @staticmethod
    def _resolve_button_key(raw: str, quick: list[dict]) -> str:
        """Convert button TEXT → KEY."""
        if not quick:
            return raw

        for btn in quick:
            if raw == btn.get("text"):
                return btn.get("key")

        return raw

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
