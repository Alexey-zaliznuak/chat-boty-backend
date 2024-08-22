from fastapi import Query
from pydantic import BaseModel
from typing import Generic, TypeVar, List

T = TypeVar("T")


def get_pagination_params(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100)) -> 'PaginationParams':
    return PaginationParams(page=page, size=size)


class PaginationParams(BaseModel):
    page: int = Query(1, ge=1)
    size: int = Query(10, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size

    def apply_to_query(self, query: "Query") -> "Query":
        return query.limit(self.size).offset(self.offset)


class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    page: int
    size: int
    total_items: int
    total_pages: int

    def __init__(self, data: List[T], pagination: PaginationParams, total_items: int):
        total_pages = (total_items + pagination.size - 1) // pagination.size
        super().__init__(
            data=data,
            page=pagination.page,
            size=min(len(data), pagination.size),
            total_items=total_items,
            total_pages=total_pages,
        )
