"""Pagination models and helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Iterable, Iterator, Sequence, TypeVar


@dataclass
class PageChunk:
    current_page: int
    page_size: int
    total: int

    @property
    def total_pages(self) -> int:
        if self.page_size <= 0:
            return 0
        pages, remainder = divmod(self.total, self.page_size)
        return pages + (1 if remainder else 0)


T = TypeVar("T")


class PagedResult(Generic[T]):
    """Wrap results returned alongside pagination metadata."""

    def __init__(self, items: Sequence[T], page: PageChunk) -> None:
        self.items = list(items)
        self.page = page

    def __iter__(self) -> Iterator[T]:
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)


def iter_pages(fetch: Iterable[PagedResult[T]]) -> Iterator[T]:
    for page in fetch:
        yield from page
