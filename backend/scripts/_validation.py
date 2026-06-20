"""Shared helpers for LeadFlow validation scripts."""

from __future__ import annotations

import sys
import traceback
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterator

from bootstrap import app_context as bootstrapped_app_context
from bootstrap import load_dotenv


BACKEND_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = BACKEND_DIR.parent

for path in (str(BACKEND_DIR), str(PROJECT_DIR)):
    if path not in sys.path:
        sys.path.insert(0, path)


@dataclass
class CheckResult:
    """Result returned by every validation check."""

    name: str
    passed: bool
    details: list[str]
    error: str | None = None
    stack_trace: str | None = None

    @property
    def status(self) -> str:
        return "PASS" if self.passed else "FAIL"


def run_validation(name: str, check: Callable[[], list[str] | None]) -> CheckResult:
    """Run one validation check and convert exceptions into structured failures."""
    load_dotenv()
    try:
        details = check() or []
        return CheckResult(name=name, passed=True, details=details)
    except Exception as exc:
        return CheckResult(
            name=name,
            passed=False,
            details=[],
            error=f"{type(exc).__name__}: {exc}",
            stack_trace=traceback.format_exc(),
        )


def print_result(result: CheckResult) -> None:
    """Print a single check result with details and diagnostics."""
    print(f"{result.name}: {result.status}")
    for detail in result.details:
        print(f"  - {detail}")
    if not result.passed:
        print(f"Root cause: {result.error}")
        print("Stack trace:")
        print(result.stack_trace)


@contextmanager
def app_context() -> Iterator:
    """Create a validated LeadFlow app context using the configured database."""
    with bootstrapped_app_context(verify_schema=True) as app:
        yield app


def cleanup_records(*records) -> None:
    """Best-effort deletion for records created by validations."""
    from database.extensions import db

    for record in records:
        if record is None:
            continue
        try:
            attached = db.session.merge(record)
            db.session.delete(attached)
            db.session.commit()
        except Exception:
            db.session.rollback()
