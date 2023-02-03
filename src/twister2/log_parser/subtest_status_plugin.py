from __future__ import annotations

import pytest
from pytest_subtests import SubTestReport


@pytest.hookimpl(tryfirst=True)
def pytest_report_teststatus(report, config):
    if report.when != 'call' or not isinstance(report, SubTestReport):
        return

    if hasattr(report, 'wasxfail'):
        return None

    outcome = report.outcome
    if report.passed:
        if config.option.verbose == 1:
            return f'subtests {outcome}', '', ''
        else:
            return f'subtests {outcome}', ',', 'SUBPASS'
    elif report.skipped:
        return outcome, '-', 'SUBSKIP'
    elif outcome == 'failed':
        return outcome, 'u', 'SUBFAIL'
