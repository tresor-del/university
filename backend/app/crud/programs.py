from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.university import Program
from app.schemas.university import (
    ProgramCreate,
    ProgramResponse,
    ProgramsResponse,
    ProgramUpdate,
)


def read_programs(*, db: Session, skip: int, limit: int) -> ProgramsResponse:
    count_statement = select(func.count()).select_from(Program)
    count = db.execute(count_statement).scalar()
    
    statement = select(Program).offset(skip).limit(limit)
    data = db.execute(statement).scalars().all()
    return ProgramsResponse.model_validate({"data": data, "count": count})

def create_program(*, db: Session, program_data: ProgramCreate) -> ProgramResponse:
    validate_data = program_data.model_dump()
    program = Program(**validate_data)
    db.add(program)
    db.commit()
    db.refresh(program)
    return ProgramResponse.model_validate(program)

def update_program(*, db: Session, program_id: UUID, data: ProgramUpdate) -> ProgramResponse | None:
    program = db.get(Program, program_id)
    if program:
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(program, key, value)
        db.commit()
        db.refresh(program)
        return ProgramResponse.model_validate(program)
    return None

def delete_program(*, db: Session, program_id: UUID) -> bool:
    program = db.get(Program, program_id)
    if program:
        db.delete(program)
        db.commit()
        return True
    return False

def get_program(*, db: Session, program_id: UUID) -> Program | None:
    statement = select(Program).where(Program.id == program_id)
    program = db.execute(statement).scalar_one_or_none()
    return program