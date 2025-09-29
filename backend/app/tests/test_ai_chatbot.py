from unittest.mock import patch, MagicMock

import pytest
from sqlalchemy.orm import Session

from app.services.ai_chatbot import get_university_context, get_chat_response
from app.crud import programs as crud_programs, departements as crud_departments, courses as crud_courses, faculty as crud_faculty
from app.schemas.university import ProgramCreate, DepartmentCreate, CourseCreate, FacultyCreate

from app.core.settings import settings


@pytest.fixture(scope="function")
def setup_university_data(db: Session):
    """Fixture pour peupler la base de données avec des données de test."""
    # 1. Créer une faculté
    faculty1 = crud_faculty.create_faculty(db=db, faculty_data=FacultyCreate(nom="Sciences et Technologies"))

    # 2. Créer un département lié à la faculté
    department1 = crud_departments.create_departement(db=db, departement_data=DepartmentCreate(nom="Informatique", id_faculte=faculty1.id))

    # 3. Créer un programme (parcours) lié au département
    program1 = crud_programs.create_program(db=db, program_data=ProgramCreate(
        nom="Génie Logiciel",
        description="Apprenez à construire des logiciels robustes.",
        niveau="Licence",
        duree=3,
        id_departement=department1.id
    ))

    # 4. Créer un cours lié au programme
    course1 = crud_courses.create_course(db=db, course_data=CourseCreate(
        titre="Algorithmique",
        description="Bases de l'algorithmique.",
        code="CS101",
        credits=5,
        id_parcours=program1.id
    ))
    
    return {
        "program": program1,
        "department": department1,
        "course": course1
    }

def test_get_university_context(db: Session, setup_university_data):
    """
    Test que le contexte de l'université est correctement généré à partir des données en base.
    """
    context = get_university_context(db)

    # Vérifie que les informations créées par la fixture sont présentes dans le contexte
    assert "Filières Disponibles" in context
    assert "Génie Logiciel" in context
    assert "Apprenez à construire des logiciels robustes." in context
    
    assert "Départements" in context
    assert "Informatique" in context
    
    assert "Exemples de Cours" in context
    assert "Algorithmique" in context
    assert "Bases de l'algorithmique" in context

def test_get_university_context_empty_db(db: Session):
    """
    Test le comportement de get_university_context avec une base de données vide.
    """
    context = get_university_context(db)
    
    assert "### Filières Disponibles\n\n" in context
    assert "### Départements\n\n" in context
    assert "### Exemples de Cours\n\n" in context


@patch('app.services.ai_chatbot.InferenceClient')
def test_get_chat_response_success(mock_inference_client, db: Session, setup_university_data):
    """
    Test la fonction get_chat_response en simulant une réponse réussie de l'API.
    """
    # Configuration du mock
    mock_api_response = "Bonjour ! La filière Génie Logiciel est excellente pour vous."
    mock_instance = MagicMock()
    mock_instance.text_generation.return_value = mock_api_response
    mock_inference_client.return_value = mock_instance

    user_question = "Parle-moi du génie logiciel."
    response = get_chat_response(db=db, user_question=user_question)

    # Vérifications
    mock_inference_client.assert_called_once_with(token=settings.HUGGINGFACE_API_KEY)
    mock_instance.text_generation.assert_called_once()
    
    # Vérifier que le prompt contient bien le contexte et la question
    call_args, call_kwargs = mock_instance.text_generation.call_args
    prompt = call_kwargs.get("prompt")
    assert "Génie Logiciel" in prompt # Vérifie que le contexte est bien passé
    assert user_question in prompt # Vérifie que la question de l'utilisateur est là

    assert response == mock_api_response


@patch('app.services.ai_chatbot.InferenceClient')
def test_get_chat_response_api_error(mock_inference_client, db: Session):
    """
    Test la gestion d'erreur lorsque l'API de Hugging Face lève une exception.
    """
    # Configuration du mock pour lever une exception
    error_message = "API is down"
    mock_instance = MagicMock()
    mock_instance.text_generation.side_effect = Exception(error_message)
    mock_inference_client.return_value = mock_instance

    user_question = "Une question au hasard"
    response = get_chat_response(db=db, user_question=user_question)

    # Vérifications
    mock_inference_client.assert_called_once()
    mock_instance.text_generation.assert_called_once()
    
    assert "Désolé, le service de chatbot rencontre une erreur" in response
    assert error_message in response