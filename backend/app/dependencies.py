from app.database.config import sessionLocal, engine, Base

# Créer toutes les tables dans la base qui sont décrites par les classes héritant de Base
Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()