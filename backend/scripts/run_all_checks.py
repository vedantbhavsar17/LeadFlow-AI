"""Run the complete LeadFlow validation suite."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

from _validation import CheckResult, print_result
from bootstrap import (
    MigrationsNotAppliedError,
    app_context,
    startup_lines,
    verify_required_tables,
)


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))


CHECKS = [
    ("database", "test_database"),
    ("api", "test_api"),
    ("nim", "test_nim"),
    ("smtp", "test_email_smtp"),
    ("imap", "test_email_imap"),
    ("conversation", "test_conversation_flow"),
    ("journey", "test_journey"),
    ("analytics", "test_analytics"),
    ("e2e", "test_e2e"),
]


REPORT_LABELS = {
    "Database": "Database",
    "API": "API",
    "NIM": "NIM",
    "SMTP": "SMTP",
    "IMAP": "IMAP",
    "Conversation": "Conversation",
    "Journey": "Journey",
    "Analytics": "Analytics",
    "E2E": "E2E",
}


def run_all() -> list[CheckResult]:
    """Execute every validation check and continue after failures."""
    print("LeadFlow validation startup")
    print("---------------------------")
    try:
        with app_context(verify_schema=False) as app:
            for line in startup_lines(app):
                print(line)
            verify_required_tables()
            print("schema status: required tables present")
    except MigrationsNotAppliedError as exc:
        print(str(exc))
        print("schema status: migrations missing")
    except Exception as exc:
        print(f"startup error: {type(exc).__name__}: {exc}")
    print()

    results: list[CheckResult] = []
    for _key, module_name in CHECKS:
        module = importlib.import_module(module_name)
        result = module.run_check()
        results.append(result)
        print_result(result)
        print()
    return results


def print_report(results: list[CheckResult]) -> None:
    """Print the required final validation report."""
    result_by_name = {result.name: result for result in results}
    print("====================================")
    print("LeadFlow Validation Report")
    print("====================================")
    for result_name, label in REPORT_LABELS.items():
        result = result_by_name.get(result_name)
        status = result.status if result else "FAIL"
        print(f"{label:<14}{status}")
    print()
    print("Overall:")
    print("READY FOR FRONTEND" if all(result.passed for result in results) else "NOT READY")


def main() -> int:
    results = run_all()
    print_report(results)
    return 0 if all(result.passed for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
