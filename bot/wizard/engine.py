from __future__ import annotations
from typing import Optional, Any, Tuple

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
    """High-level dialog controller."""

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

        log.info(f"[Wizard] Initialized (country={country}, lang={lang})")
        log.debug(f"[Wizard] Steps initialized: {[s.key for s in self.queue.steps]}")

    # -------------------------------------------------------------
    # CURRENT STEP
    # -------------------------------------------------------------
    def current_step(self) -> Optional[Step]:
        try:
            step = self.queue.current()
            log.debug(f"[Wizard] current_step → {step.key if step else None}")
            return step
        except QueueError as e:
            log.error(f"[Wizard] current_step ERROR: {e}")
            return None

    # -------------------------------------------------------------
    # NEXT STEP
    # -------------------------------------------------------------
    def next_step(self) -> Tuple[bool, Optional[Step], str]:
        try:
            step = self.queue.next()
            log.debug(f"[Wizard] next_step → {step.key if step else None}")
            return True, step, "ok"

        except InvalidNavigationError as e:
            log.warning(f"[Wizard] Invalid next navigation: {e}")
            return False, None, "navigation_error"

        except QueueError as e:
            log.error(f"[Wizard] next_step queue error: {e}")
            return False, None, "queue_error"

        except Exception as e:
            log.error(f"[Wizard] next_step fatal error: {e}", exc_info=True)
            return False, None, "fatal_error"

    # -------------------------------------------------------------
    # PREVIOUS STEP
    # -------------------------------------------------------------
    def prev_step(self) -> Tuple[bool, Optional[Step], str]:
        try:
            step = self.queue.previous()
            log.debug(f"[Wizard] prev_step → {step.key if step else None}")
            return True, step, "ok"

        except InvalidNavigationError as e:
            log.warning(f"[Wizard] Invalid previous navigation: {e}")
            return False, None, "navigation_error"

        except QueueError as e:
            log.error(f"[Wizard] prev_step queue error: {e}")
            return False, None, "queue_error"

        except Exception as e:
            log.error(f"[Wizard] prev_step fatal error: {e}", exc_info=True)
            return False, None, "fatal_error"

    # -------------------------------------------------------------
    # PROCESS ANSWER
    # -------------------------------------------------------------
    def process_answer(self, key: str, raw_value, display_value: str) -> Tuple[bool, str]:
        try:
            log.debug(f"[Wizard] process_answer key={key} raw={raw_value}")

            # FILES → do NOT normalize
            if isinstance(raw_value, (dict, list)):
                normalized = raw_value
            else:
                normalized = self._normalize_answer(raw_value)

            self.queue.set_answer(key, normalized, display_value)
            return True, "ok"

        except BranchConfigError as e:
            log.error(f"[Wizard] Branch error for key={key}: {e}")
            return False, "branch_error"

        except QueueError as e:
            log.error(f"[Wizard] QueueError for key={key}: {e}")
            return False, "queue_error"

        except Exception as e:
            log.error(f"[Wizard] Fatal process_answer error: {e}", exc_info=True)
            return False, "fatal_error"

    # -------------------------------------------------------------
    # VALIDATE INPUT
    # -------------------------------------------------------------
    async def validate_input(self, step_key: str, raw_value):
        log.debug(f"[Wizard] validate_input step={step_key} type={type(raw_value)}")

        locale = L10N.get(self.lang, {})
        steps = locale.get("steps", {})
        by_country = locale.get("steps_by_country", {}).get(self.country, {})
        cfg = by_country.get(step_key, {}) or steps.get(step_key, {})

        validator_key = cfg.get("validator")

        # TYPE CHECK
        ok_type, type_error = self._check_expected_type(cfg, raw_value)
        if not ok_type:
            return False, "", type_error

        # -------------------------------------------------------
        # FILE UPLOAD MODE — skip normalize, skip text logic
        # -------------------------------------------------------
        if isinstance(raw_value, (dict, list)):
            from services.validators import VALIDATOR_REGISTRY
            validator = VALIDATOR_REGISTRY.get(validator_key)

            if not validator:
                return True, raw_value, "Документ"

            try:
                ok, result = await validator(raw_value)
            except Exception as e:
                log.error(f"[Wizard] File validator error: {e}", exc_info=True)
                return False, "", "Ошибка файла"

            if not ok:
                return False, "", cfg.get("validator_error") or result

            canonical = raw_value
            display = "Документ" if isinstance(raw_value, dict) else f"{len(raw_value)} файлов"
            return True, canonical, display

        # -------------------------------------------------------
        # TEXT MODE
        # -------------------------------------------------------
        raw_norm = self._normalize_answer(raw_value)

        quick = cfg.get("quick") or []
        raw_norm = self._resolve_button_key(raw_norm, quick)

        # no validator → accept
        if not validator_key:
            return True, raw_norm, raw_norm

        from services.validators import VALIDATOR_REGISTRY
        validator = VALIDATOR_REGISTRY.get(validator_key)

        if not validator:
            return False, "", f"Missing validator '{validator_key}'"

        # ENUM special case
        if validator_key == "enum":
            allowed = [btn.get("key") for btn in quick]

            try:
                ok, result = await validator(raw_norm, allowed)
            except Exception as e:
                log.error(f"[Wizard] Enum validator error: {e}", exc_info=True)
                return False, "", "Ошибка валидации"
        else:
            try:
                ok, result = await validator(raw_norm)
            except Exception as e:
                log.error(f"[Wizard] Validator error: {e}", exc_info=True)
                return False, "", "Ошибка валидации"

        if not ok:
            return False, "", cfg.get("validator_error") or result

        canonical = result
        display = canonical

        for btn in quick:
            if btn.get("key") == canonical:
                display = btn.get("text", canonical)
                break

        return True, canonical, display

    # -------------------------------------------------------------
    # UNIFIED STEP CONFIG RESOLVER
    # -------------------------------------------------------------
    def get_step_cfg(self, step_key: str) -> dict:
        """
        Returns merged step config:
        - steps_by_country[country][key]
        - OR steps[key]
        Exactly same logic as ProgressRouter, but centralized.
        """
        locale = L10N.get(self.lang, {})
        steps = locale.get("steps", {})
        by_country = locale.get("steps_by_country", {}).get(self.country, {})

        cfg = by_country.get(step_key, {}) or steps.get(step_key, {}) or {}

        # Always return dict
        if not isinstance(cfg, dict):
            return {}

        return cfg

    # -------------------------------------------------------------
    # TYPE CHECK
    # -------------------------------------------------------------
    @staticmethod
    def _check_expected_type(step_cfg: dict, raw_value: Any) -> Tuple[bool, str]:
        expected = step_cfg.get("expected_type", "text")

        if expected == "any":
            return True, ""

        if expected == "file":
            if isinstance(raw_value, dict):
                return True, ""
            if isinstance(raw_value, list) and all(isinstance(x, dict) for x in raw_value):
                return True, ""
            return False, step_cfg.get("validator_error", "Прикрепите документ.")

        if expected == "text":
            return isinstance(raw_value, str), step_cfg.get("validator_error", "Введите текст.")

        return True, ""

    # -------------------------------------------------------------
    # NORMALIZER — FILE SAFE
    # -------------------------------------------------------------
    def _normalize_answer(self, answer: str) -> Any:
        """Normalize yes/no; return raw for everything else."""
        try:
            if not isinstance(answer, str):
                return answer  # SAFETY: prevents .lower() crash

            local_yes = t(self.lang, "common.yes").lower()
            local_no = t(self.lang, "common.no").lower()

            a = answer.lower().strip()

            if a == local_yes:
                return "Yes"
            if a == local_no:
                return "No"

            return answer

        except Exception as e:
            log.error(f"[Wizard] normalize_answer error: {e}", exc_info=False)
            return answer

    @staticmethod
    def _resolve_button_key(raw: str, quick: list[dict]) -> str:
        if not quick:
            return raw
        for btn in quick:
            if raw == btn.get("text"):
                return btn.get("key")
        return raw

    # -------------------------------------------------------------
    # FINISHED?
    # -------------------------------------------------------------
    def is_finished(self) -> bool:
        return self.queue.is_finished()
