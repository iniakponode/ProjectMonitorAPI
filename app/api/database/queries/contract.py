# app/database/queries/contract.py
from sqlalchemy.orm import Session
from app.api.database.models import Contract


def create_contract(db: Session, contract_data: dict):
    contract = Contract(**contract_data)
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return contract


def get_contract_by_id(db: Session, contract_id: int):
    return db.query(Contract).filter(Contract.id == contract_id).first()
