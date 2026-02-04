"""Utility helpers for deterministic extraction behavior."""

from __future__ import annotations

from typing import Iterable, TypeVar

T = TypeVar("T")


def dedupe_preserve_order(items: Iterable[T]) -> list[T]:
    """Return unique items while preserving first-seen order."""
    seen: set[T] = set()
    result: list[T] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result
