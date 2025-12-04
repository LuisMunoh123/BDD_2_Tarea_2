"""Database models for the library management system."""

from dataclasses import dataclass
from datetime import date, datetime

from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy import Column, ForeignKey, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


book_categories = Table(
    "book_categories",
    BigIntAuditBase.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"), primary_key=True),
)


class User(BigIntAuditBase):
    """User model with audit fields."""

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)
    fullname: Mapped[str]
    password: Mapped[str]

    loans: Mapped[list["Loan"]] = relationship(back_populates="user")
    reviews: Mapped[list["Review"]] = relationship(back_populates="user")

class Book(BigIntAuditBase):
    """Book model with audit fields."""

    __tablename__ = "books"

    title: Mapped[str] = mapped_column(unique=True)
    author: Mapped[str]
    isbn: Mapped[str] = mapped_column(unique=True)
    pages: Mapped[int]
    published_year: Mapped[int]

    loans: Mapped[list["Loan"]] = relationship(back_populates="book")
    reviews: Mapped[list["Review"]] = relationship(back_populates="book")
    
    # relación many-to-many con Category
    categories: Mapped[list["Category"]] = relationship(
        "Category",
        secondary=book_categories,
        back_populates="books",
    )


class Category(BigIntAuditBase):
    """Category model with audit fields."""

    __tablename__ = "categories"

    # BigIntAuditBase ya define id, created_at, updated_at, etc.
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    books: Mapped[list["Book"]] = relationship(
        "Book",
        secondary=book_categories,
        back_populates="categories",
    )


class Loan(BigIntAuditBase):
    """Loan model with audit fields."""

    __tablename__ = "loans"

    loan_dt: Mapped[date] = mapped_column(default=datetime.today)
    return_dt: Mapped[date | None]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))

    user: Mapped[User] = relationship(back_populates="loans")
    book: Mapped[Book] = relationship(back_populates="loans")


class Review(BigIntAuditBase):
    """Review model for book ratings and comments."""

    __tablename__ = "reviews"

    rating: Mapped[int]
    comment: Mapped[str]
    review_date: Mapped[date] = mapped_column(default=date.today)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))

    user: Mapped["User"] = relationship(back_populates="reviews")
    book: Mapped["Book"] = relationship(back_populates="reviews")


@dataclass
class PasswordUpdate:
    """Password update request."""

    current_password: str
    new_password: str


@dataclass
class BookStats:
    """Book statistics data."""

    total_books: int
    average_pages: float
    oldest_publication_year: int | None
    newest_publication_year: int | None
