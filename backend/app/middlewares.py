from fastapi.middleware.cors import CORSMiddleware

from database.config import get_settings

settings = get_settings()

def setup_middleware(app):

    # cors middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.origins, 
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)