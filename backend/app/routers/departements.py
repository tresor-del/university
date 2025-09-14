from uuid import UUID
from fastapi import Depends, dependencies
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException

from app.deps import get_current_active_admin, SessionDeps
from app.schemas.university import DepartementsResponse, DepartmentResponse, DepartmentCreate, DepartmentUpdate
from app.schemas.message import Message
from app.models.university import Department
from app.crud.departements import (
    read_departement,
    create_departement,
    update_departement,
    delete_department,
    get_departement
)

router = APIRouter(prefix="/departments", tags=["departments"])



@router.get("/", dependencies=[Depends(get_current_active_admin)], response_model=DepartementsResponse)
def read_departement_route(db: SessionDeps, skip: int = 0, limit: int = 100) -> DepartementsResponse:
    """
    Récupérer la liste de tous les departements
    """
    department = read_departement(db=db, skip=skip, limit=limit)
    return department

@router.post("/", dependencies=[Depends(get_current_active_admin)], response_model=DepartmentResponse)
def create_departemnt_route(db: SessionDeps, data: DepartmentCreate) -> DepartmentResponse:
    """
    creéer un departement
    """
    departement = create_departement(db=db, department_data=data)
    return departement

@router.patch("/{department_id}", dependencies=[Depends(get_current_active_admin)], response_model=DepartmentResponse)
def update_department_route(db: SessionDeps, department_id: UUID, data: DepartmentUpdate) -> DepartmentResponse:
    """
    Met à jour un departement
    """
    departement = db.get(Department, department_id)
    if not departement:
        raise HTTPException(
            status_code=404,
            detail="Departement non trouvé sur le système"
        )
    department_updated = update_departement(db=db, department_id=department_id, data=data)
    return department_updated

@router.delete("/{department_id}", dependencies=[Depends(get_current_active_admin)], response_model=Message)
def delete_department_route(db: SessionDeps, department_id: UUID) -> Message:
    """
    Supprime un Departement
    """
    result = delete_department(db=db, department_id=department_id)
    if result:
        return Message("Departement supprimé avec succès")
    raise HTTPException(
            status_code=404,
            detail="Departement non trouvé sur le système"
        )

@router.get("/{department_id}", dependencies=[Depends(get_current_active_admin)], response_model=DepartmentResponse)
def get_department_route(db: SessionDeps, department_id: UUID) -> DepartmentResponse:
    """
    Récupérer un Departement
    """
    departement = get_departement(db=db, department_id=department_id)
    if departement:
        return departement
    raise HTTPException(
        status_code=404,
        detail="Departement non trouvé sur le système"
    )
