"""Repository for Book database operations."""

from collections.abc import Sequence

from advanced_alchemy.repository import SQLAlchemySyncRepository
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Book, Category, Review


class BookRepository(SQLAlchemySyncRepository[Book]):
    """Repository for book database operations."""

    model_type = Book

    def get_available_books(self) -> Sequence[Book]:
        """Retornar libros con stock > 0."""
        stmt = select(Book).where(Book.stock > 0)
        return self.session.scalars(stmt).all()

    def find_by_category(self, category_id: int) -> Sequence[Book]:
        """Buscar libros que pertenecen a una categoría dada."""
        stmt = (
            select(Book)
            .join(Book.categories)
            .where(Category.id == category_id)
        )
        return self.session.scalars(stmt).all()

    def get_most_reviewed_books(self, limit: int = 10) -> Sequence[Book]:
        """Libros ordenados por cantidad de reseñas (descendente)."""
        review_count = func.count(Review.id).label("review_count")

        stmt = (
            select(Book)
            .outerjoin(Review, Review.book_id == Book.id)
            .group_by(Book.id)
            .order_by(review_count.desc())
            .limit(limit)
        )
        return self.session.scalars(stmt).all()

    def update_stock(self, book_id: int, quantity: int) -> Book:
        """Actualizar el stock de un libro, validando que no quede negativo.

        Aquí interpretamos que `quantity` es el NUEVO stock.
        """
        book = self.session.get(Book, book_id)
        if book is None:
            raise ValueError(f"Book with id {book_id} not found.")

        if quantity < 0:
            raise ValueError("El stock no puede ser negativo.")

        book.stock = quantity

        self.session.add(book)
        if getattr(self, "auto_commit", False):
            self.session.commit()
        else:
            self.session.flush()

        return book

    def search_by_author(self, author_name: str) -> Sequence[Book]:
        """Buscar libros por autor (búsqueda parcial, case-insensitive)."""
        pattern = f"%{author_name}%"
        stmt = select(Book).where(Book.author.ilike(pattern))
        return self.session.scalars(stmt).all()


async def provide_book_repo(db_session: Session) -> BookRepository:
    """Provide book repository instance with auto-commit."""
    return BookRepository(session=db_session, auto_commit=True)
