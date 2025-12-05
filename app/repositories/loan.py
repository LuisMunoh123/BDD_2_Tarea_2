"""Repository for Loan database operations."""

from collections.abc import Sequence
from datetime import date
from decimal import Decimal

from advanced_alchemy.repository import SQLAlchemySyncRepository
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Loan, LoanStatus


class LoanRepository(SQLAlchemySyncRepository[Loan]):
    """Repository for loan database operations."""

    model_type = Loan

    def get_active_loans(self) -> Sequence[Loan]:
        """Préstamos con status == ACTIVE."""
        stmt = select(Loan).where(Loan.status == LoanStatus.ACTIVE)
        return self.session.scalars(stmt).all()

    def get_overdue_loans(self) -> Sequence[Loan]:
        """
        Préstamos vencidos: due_date pasada y status == ACTIVE.
        Además, actualiza su status a OVERDUE.
        """
        today = date.today()

        stmt = (
            select(Loan)
            .where(
                Loan.status == LoanStatus.ACTIVE,
                Loan.due_date.is_not(None),
                Loan.due_date < today,
            )
        )

        overdue_loans = self.session.scalars(stmt).all()

        for loan in overdue_loans:
            loan.status = LoanStatus.OVERDUE

        if overdue_loans:
            self.session.add_all(overdue_loans)
            if getattr(self, "auto_commit", False):
                self.session.commit()
            else:
                self.session.flush()

        return overdue_loans

    def calculate_fine(self, loan_id: int) -> Decimal:
        """
        Calcular multa: $500 por día de retraso.
        Se calcula en base a hoy y la due_date.
        """
        loan = self.session.get(Loan, loan_id)
        if loan is None:
            raise ValueError(f"Loan with id {loan_id} not found.")

        if loan.due_date is None:
            return Decimal("0.00")

        today = date.today()
        days_late = (today - loan.due_date).days

        if days_late <= 0:
            return Decimal("0.00")

        return Decimal(days_late) * Decimal("500.00")

    def return_book(self, loan_id: int) -> Loan:
        """
        Procesar devolución:
        - status -> RETURNED
        - return_dt -> fecha actual
        - fine_amount -> calcular y guardar si corresponde
        - incrementar stock del libro asociado
        """
        loan = self.session.get(Loan, loan_id)
        if loan is None:
            raise ValueError(f"Loan with id {loan_id} not found.")

        today = date.today()
        loan.return_dt = today

        # Calcular multa en base a la due_date
        fine = Decimal("0.00")
        if loan.due_date is not None:
            days_late = (today - loan.due_date).days
            if days_late > 0:
                fine = Decimal(days_late) * Decimal("500.00")

        loan.fine_amount = fine
        loan.status = LoanStatus.RETURNED

        # Incrementar stock del libro
        if loan.book is not None:
            loan.book.stock = (loan.book.stock or 0) + 1

        self.session.add(loan)
        if getattr(self, "auto_commit", False):
            self.session.commit()
        else:
            self.session.flush()

        return loan

    def get_user_loan_history(self, user_id: int) -> Sequence[Loan]:
        """Historial completo de préstamos de un usuario ordenado por fecha."""
        stmt = (
            select(Loan)
            .where(Loan.user_id == user_id)
            .order_by(Loan.loan_dt.desc())
        )
        return self.session.scalars(stmt).all()


async def provide_loan_repo(db_session: Session) -> LoanRepository:
    """Provide loan repository instance with auto-commit."""
    return LoanRepository(session=db_session, auto_commit=True)
