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

def upload_file(uid, filename, upload_time, finish_time, status, user_id):
    """
    adding an upload file to the database for the user
    :param uid: file's uid
    :param filename: file name
    :param upload_time: upload time
    :param finish_time: finish time
    :param status: upload status
    :param user_id: user id
    """
    # Create a new User object
    file = db.Upload(uid=uid, filename=filename, upload_time=upload_time, finish_time=finish_time, status=status ,user_id=user_id)
    session.add(file)
    session.commit()



def delete_file(uid):
    """
    delete the file from the database using the uid
    :param uid: file's uid
    """
    file = session.query(db.Upload).filter_by(uid=uid).first()
    if file:
        session.delete(file)
        session.commit()
