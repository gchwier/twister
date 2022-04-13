from __future__ import annotations

import logging

import pytest

from twister2.filter.filter_interface import FilterInterface
from twister2.filter.slow_test_filter import SlowTestFilter
from twister2.filter.tag_filter import TagFilter

logger = logging.getLogger(__name__)


class FilterPlugin:
    """Plugin for filtering tests."""

    def __init__(self, config: pytest.Config):
        self.config = config
        self._filters: list[FilterInterface] = [
            SlowTestFilter(self.config),
        ]

    def add_filter(self, filter_: FilterInterface) -> None:
        if filter_ not in self._filters:
            self._filters.append(filter_)

    @pytest.hookimpl(tryfirst=True)
    def pytest_collection_modifyitems(
        self, session: pytest.Session, config: pytest.Config, items: list[pytest.Item]
    ):
        selected_items: list[pytest.Item] = []
        deselected_items: list[pytest.Item] = []

        for item in items:
            for filter_ in self._filters:
                if filter_.filter(item):
                    deselected_items.append(item)
                    break
                else:
                    selected_items.append(item)
                    break

        if deselected_items:
            config.hook.pytest_deselected(items=deselected_items)
        items[:] = selected_items
