"""Controller for Loan endpoints."""

from datetime import timedelta
from decimal import Decimal
from typing import Sequence

from advanced_alchemy.exceptions import DuplicateKeyError, NotFoundError
from litestar import Controller, delete, get, patch, post
from litestar.di import Provide
from litestar.dto import DTOData
from litestar.exceptions import HTTPException

from app.controllers import duplicate_error_handler, not_found_error_handler
from app.dtos.loan import LoanCreateDTO, LoanReadDTO, LoanUpdateDTO
from app.models import Loan, LoanStatus
from app.repositories.loan import LoanRepository, provide_loan_repo


class LoanController(Controller):
    """Controller for loan management operations."""

    path = "/loans"
    tags = ["loans"]
    return_dto = LoanReadDTO
    dependencies = {"loans_repo": Provide(provide_loan_repo)}
    exception_handlers = {
        NotFoundError: not_found_error_handler,
        DuplicateKeyError: duplicate_error_handler,
    }

    @get("/")
    async def list_loans(self, loans_repo: LoanRepository) -> Sequence[Loan]:
        """Get all loans."""
        return loans_repo.list()

    @get("/{id:int}")
    async def get_loan(self, id: int, loans_repo: LoanRepository) -> Loan:
        """Get a loan by ID."""
        return loans_repo.get(id)

    @post("/", dto=LoanCreateDTO)
    async def create_loan(
        self,
        data: DTOData[Loan],
        loans_repo: LoanRepository,
    ) -> Loan:
        """Create a new loan."""
        loan = data.create_instance()

        if loan.loan_dt is None:
            raise HTTPException(status_code=400, detail="loan_dt es obligatorio")

        # due_date = loan_dt + 14 días
        loan.due_date = loan.loan_dt + timedelta(days=14)

        # status por defecto ACTIVE (doble seguridad, además del default del modelo)
        loan.status = LoanStatus.ACTIVE

        # la multa se calcula después, así que por ahora None
        loan.fine_amount = None

        return loans_repo.add(loan)

    @patch("/{id:int}", dto=LoanUpdateDTO)
    async def update_loan(
        self,
        id: int,
        data: DTOData[Loan],
        loans_repo: LoanRepository,
    ) -> Loan:
        """Update a loan by ID."""
        loan, _ = loans_repo.get_and_update(match_fields="id", id=id, **data.as_builtins())

        return loan

    @delete("/{id:int}")
    async def delete_loan(self, id: int, loans_repo: LoanRepository) -> None:
        """Delete a loan by ID."""
        loans_repo.delete(id)

    @get("/active")
    async def get_active_loans(self, loans_repo: LoanRepository) -> list[Loan]:
        """Listar préstamos activos."""
        return list(loans_repo.get_active_loans())

    @get("/overdue")
    async def get_overdue_loans(self, loans_repo: LoanRepository) -> list[Loan]:
        """
        Listar préstamos vencidos.
        Esta operación también actualiza el status a OVERDUE en la base de datos.
        """
        return list(loans_repo.get_overdue_loans())

    @get("/user/{user_id:int}")
    async def get_user_loan_history(self, user_id: int, loans_repo: LoanRepository) -> list[Loan]:
        """Historial de préstamos de un usuario."""
        return list(loans_repo.get_user_loan_history(user_id=user_id))

    @post("/{loan_id:int}/return")
    async def return_loan(self, loan_id: int, loans_repo: LoanRepository) -> Loan:
        """Procesar devolución de un préstamo."""
        return loans_repo.return_book(loan_id=loan_id)

    @get("/{loan_id:int}/fine", return_dto=None)
    async def get_loan_fine(self, loan_id: int, loans_repo: LoanRepository) -> dict:
        """Calcular y mostrar la multa de un préstamo."""
        fine: Decimal = loans_repo.calculate_fine(loan_id=loan_id)
        return {
            "loan_id": loan_id,
            "fine_amount": str(fine),
        }
