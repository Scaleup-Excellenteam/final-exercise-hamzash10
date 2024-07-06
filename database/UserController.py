from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
import db_models as db

# binding the database to be able to access it
DB_NAME = "mydatabase.db"
engine = create_engine(f"sqlite:///{DB_NAME}", echo=True)
SessionLocal = sessionmaker(bind=engine)

if not os.path.exists(DB_NAME):
    db.Base.metadata.create_all(bind=engine)  # Ensure tables are created if they don't exist

# start the session
session = SessionLocal()

def add_user(user_email):
    """
    adding a user to the database
    :param user_email: the user's email
    """
    # Create a new User object
    user = db.User(email=user_email)
    session.add(user)
    session.commit()

def delete_user(user_id):
    """
    deleting a user from the database
    :param user_id:
    :return: ?
    """
    user = session.query(db.User).filter_by(id=user_id).first()
    if user:
        session.delete(user)
        session.commit()

