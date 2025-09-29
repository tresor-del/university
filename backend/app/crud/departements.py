from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.schemas.university import (
    DepartmentCreate,
    DepartmentResponse,
    DepartementsResponse,
    DepartmentUpdate,
)
from app.models.university import Department



def read_departement(*, db: Session, skip: int, limit: int) -> dict | None:
    count_statement = select(func.count()).select_from(Department)
    count = db.execute(count_statement).scalar()
    
    statement = select(Department).offset(skip).limit(limit)
    data = db.execute(statement).scalars().all()
    return {"data": data, "count": count}

def create_departement(*, db: Session, departement_data: DepartmentCreate) -> DepartmentResponse | None:
    validated_data = departement_data.model_dump()
    departement = Department(**validated_data)
    db.add(departement)
    db.commit()
    db.refresh(departement)
    return DepartmentResponse.model_validate(departement)

def update_departement(*, db: Session, dep_id: UUID, data: DepartmentUpdate) -> DepartmentResponse | None:
    departement = db.query(Department).where(Department.id==dep_id).first()
    if departement:
        validate_data = data.model_validate()
        for key, value in validate_data:
            setattr(departement, key, value)
        db.commit()
        db.refresh(departement)
        return DepartmentResponse.model_validate(departement)
    return None

def delete_department(*, db: Session, department_id: UUID) -> DepartmentResponse | None:
    department = db.query(Department).where(department.id==department_id).first()
    if department:
        db.delete(department)
        db.commit()
        return True
    return False

def get_departement(*, db: Session, department_id: UUID) -> DepartmentResponse | None:
    statement = select(Department).where(Department.id==department_id)
    department = db.execute(statement).scalar_one()
    return department if department else None