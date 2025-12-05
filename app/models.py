"""Database models for the library management system."""

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum

from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy import Boolean, Column, Date, Enum as SAEnum, ForeignKey, Numeric, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class LoanStatus(str, Enum):
    ACTIVE = "ACTIVE"
    RETURNED = "RETURNED"
    OVERDUE = "OVERDUE"


book_categories = Table(
    "book_categories",
    BigIntAuditBase.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"), primary_key=True),
)


class User(BigIntAuditBase):
    """User model with audit fields."""

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    fullname: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

    # Nuevos campos
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(String, nullable=True)
    address: Mapped[str | None] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

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

    stock: Mapped[int] = mapped_column(default=1)
    description: Mapped[str | None] = mapped_column(nullable=True)
    language: Mapped[str] = mapped_column()
    publisher: Mapped[str | None] = mapped_column(nullable=True)

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

    loan_dt: Mapped[date] = mapped_column(Date, nullable=False, default=datetime.today)
    return_dt: Mapped[date | None] = mapped_column(Date, nullable=True)

    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    fine_amount: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2), nullable=True
    )
    status: Mapped[LoanStatus] = mapped_column(
        SAEnum(LoanStatus, name="loan_status"),
        default=LoanStatus.ACTIVE,
        server_default=LoanStatus.ACTIVE.value,
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)

    user: Mapped[User] = relationship(back_populates="loans")
    book: Mapped[Book] = relationship(back_populates="loans")


class Review(BigIntAuditBase):
    """Review model for book ratings and comments."""

    __tablename__ = "reviews"

    rating: Mapped[int] = mapped_column(nullable=False)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    review_date: Mapped[date] = mapped_column(default=datetime.today)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))

    user: Mapped[User] = relationship(back_populates="reviews")
    book: Mapped[Book] = relationship(back_populates="reviews")


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
