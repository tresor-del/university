from unittest.mock import patch, MagicMock

from sqlalchemy.orm import Session

from app.services.ia_chatbot import get_chat_response, get_university_context

from app.core.settings import settings



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


@patch('app.services.ia_chatbot.InferenceClient')
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


@patch('app.services.ia_chatbot.InferenceClient')
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