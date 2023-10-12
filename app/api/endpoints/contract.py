# app/api/endpoints/contract.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.database.base import Base, engine
from app.api.database.dependency.db_instance import get_db
from app.api.schemas.contract import ContractCreate, Contract
from app.api.database.queries.contract import create_contract, get_contract_by_id
Base.metadata.create_all(bind=engine)
router = APIRouter()


@router.post("/contracts", response_model=Contract, summary="Create a new contract")
def create_contract_endpoint(
        contract: ContractCreate,
        db: Session = Depends(get_db)
):
    """
    Create a new contract.

    This endpoint allows users to create a new contract.

    - **contract**: Contract information to create.

    Returns:
    - Created contract information.
    """
    created_contract = create_contract(db, contract.dict())
    return created_contract


@router.get("/contracts/{contract_id}", response_model=Contract, summary="Retrieve a contract")
def retrieve_contract_endpoint(
        contract_id: int,
        db: Session = Depends(get_db)
):
    """
    Retrieve a contract by ID.

    - **contract_id**: Contract's unique identifier.

    Returns:
    - Retrieved contract information.
    """
    contract = get_contract_by_id(db, contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract
