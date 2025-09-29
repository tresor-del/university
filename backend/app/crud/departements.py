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



def read_departement(*, db: Session, skip: int, limit: int) -> DepartementsResponse | None:
    count_statement = select(func.count(Department.id))
    count = db.execute(count_statement).scalar()
    
    statement = select(Department).offset(skip).limit(limit) 
    data = db.execute(statement).scalars().all()
    return DepartementsResponse.model_validate({"data": data, "count": count})

def create_departement(*, db: Session, departement_data: DepartmentCreate) -> DepartmentResponse | None:
    validated_data = departement_data.model_dump()
    departement = Department(**validated_data)
    db.add(departement)
    db.commit() 
    db.refresh(departement)
    return DepartmentResponse.model_validate(departement)

def update_departement(*, db: Session, department_id: UUID, data: DepartmentUpdate) -> DepartmentResponse | None:
    departement = db.get(Department, department_id)
    if departement:
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(departement, key, value)
        db.commit()
        db.refresh(departement)
        return DepartmentResponse.model_validate(departement)
    return None

def delete_departement(*, db: Session, department_id: UUID) -> bool:
    department = db.get(Department, department_id)
    if department:
        db.delete(department)
        db.commit()
        return True
    return False

def get_departement(*, db: Session, department_id: UUID) -> Department | None:
    statement = select(Department).where(Department.id == department_id)
    department = db.execute(statement).scalar_one_or_none()
    return department