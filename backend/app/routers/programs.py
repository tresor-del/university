from uuid import UUID
from fastapi import dependencies, Depends
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException

from app.deps import get_current_active_admin, SessionDeps
from app.models.university import Program
from app.schemas.message import Message
from app.schemas.university import ProgramCreate, ProgramUpdate, ProgramResponse, ProgramsResponse
from app.crud.programs import (
    read_programs,
    create_program,
    update_program,
    delete_program,
    get_program
)

router = APIRouter(prefix="/programs", tags=["programs"])



@router.get("/", dependencies=[Depends(get_current_active_admin)], response_model=ProgramsResponse)
def read_programs_route(db: SessionDeps, skip: int = 0, limit: int = 100) -> ProgramsResponse:
    """
    Récupérer la liste de toutes les programs
    """
    programs = read_programs(db=db, skip=skip, limit=limit)
    return programs

@router.post("/", dependencies=[Depends(get_current_active_admin)], response_model=ProgramResponse)
def create_program_route(db: SessionDeps, data: ProgramCreate) -> ProgramResponse:
    """
    creéer un program
    """
    program = create_program(db=db, program_data=data)
    return program

@router.patch("/{program_id}", dependencies=[Depends(get_current_active_admin)], response_model=ProgramResponse)
def update_program_route(db: SessionDeps, program_id: UUID, data: ProgramUpdate) -> ProgramResponse:
    """
    Mets à jour un program
    """
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(
            status_code=404,
            detail="Program non trouvé sur le système"
        )
    program_updated = update_program(db=db, program_id=program_id, data=data)
    return program_updated

@router.delete("/{program_id}", dependencies=[Depends(get_current_active_admin)], response_model=Message)
def delete_program_route(db: SessionDeps, program_id: UUID) -> Message:
    """
    Supprime un program
    """
    result = delete_program(db=db, program_id=program_id)
    if result:
        return Message("Program supprimé avec succès")
    raise HTTPException(
            status_code=404,
            detail="Program non trouvé sur le système"
        )

@router.get("/{program_id}", dependencies=[Depends(get_current_active_admin)], response_model=ProgramResponse)
def get_program_route(db: SessionDeps, program_id: UUID) -> ProgramResponse:
    """
    Récupérer un program
    """
    program = get_program(db=db, program_id=program_id)
    if program:
        return program
    raise HTTPException(
        status_code=404,
        detail="Program non trouvé sur le système"
    )
