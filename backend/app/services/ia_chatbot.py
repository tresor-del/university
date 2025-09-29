import logging
from huggingface_hub import InferenceClient
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.core.settings import settings
from app.crud import programs as crud_programs
from app.crud import courses as crud_courses
from app.crud import departements as crud_departments


logger = logging.getLogger(__name__)

def get_university_context(db: Session) -> str:
    """
    Récupère les informations sur les filières, départements et cours depuis la base de données
    pour les fournir en contexte au LLM.
    """
    try:
        # Récupérer les programmes
        programs_data = crud_programs.read_programs(db=db, skip=0, limit=100)["data"]
        programs_context = "\n".join([f"- {p.nom}: {p.description}" for p in programs_data])
        
        # Récupérer les départements
        departments_data = crud_departments.read_departement(db=db, skip=0, limit=100)["data"]
        departments_context = "\n".join([f"- {d.nom}" for d in departments_data])
        
        # Récupérer quelques cours en exemple
        courses_data = crud_courses.read_courses(db=db, skip=0, limit=20)["data"] # Limité pour ne pas surcharger
        courses_context = "\n".join([f"- {c.titre}: {c.description}" for c in courses_data])
        
        context = f"""
### Filières Disponibles
{programs_context}

### Départements
{departments_context}

### Exemples de Cours
{courses_context}
"""
        return context
    except SQLAlchemyError as e:
        logger.error(f"Erreur de base de données lors de la récupération du contexte: {e}", exc_info=True)
        return "Impossible de récupérer les informations sur les filières pour le moment."


def get_chat_response(*, db: Session, user_question: str) -> str:
    """
    Interroge l'API d'inférence de Hugging Face avec la question de l'utilisateur et le contexte de l'université.
    """
    client = InferenceClient(token=settings.HUGGINGFACE_API_KEY)
    university_context = get_university_context(db)

    # Les modèles open-source ont souvent besoin d'un format de prompt spécifique.donc ne touche pas au prompt que je rentre.
    # Celui-ci est adapté pour le modèle "Zephyr".
    prompt = f"""<|system|>
Tu es un conseiller d'orientation expert et amical pour notre université. Ta mission est d'aider les étudiants en répondant à leurs questions sur les filières. Base tes réponses EXCLUSIVEMENT sur les informations fournies dans le contexte ci-dessous. Si tu ne connais pas la réponse ou si la question sort du cadre des filières listées, dis-le poliment. Ne mentionne jamais de filières qui ne sont pas dans la liste.

--- CONTEXTE DES FILIÈRES DISPONIBLES ---
{university_context}
--- FIN DU CONTEXTE ---</s>
<|user|>
{user_question}</s>
<|assistant|>
"""

    try:
        response = client.text_generation(
            prompt=prompt,
            model="HuggingFaceH4/zephyr-7b-beta",
            max_new_tokens=250,  #c'est pour limiter la longueur de la réponse pour qu'elle ne divague pas
            temperature=0.7,
        )
        return response
    except Exception as e:
        logger.error(f"Erreur lors de l'appel à l'API de Hugging Face: {e}", exc_info=True)
        return f"Désolé, le service de chatbot rencontre une erreur : {e}"
    