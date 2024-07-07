import uuid

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, asc
import os
import database.db_models as db

# binding the database to be able to access it
DB_NAME = r'C:\Users\2022\PycharmProjects\Excellenteam\FinalProject\final-exercise-hamzash10\database\mydatabase.db'
engine = create_engine(f"sqlite:///{DB_NAME}", echo=True)
SessionLocal = sessionmaker(bind=engine)

if not os.path.exists(DB_NAME):
    db.Base.metadata.create_all(bind=engine)  # Ensure tables are created if they don't exist

# start the session
session = SessionLocal()


def get_user(user_email):
    """
    Get user by email, if it doesn't exist, create add the user to the database and return it
    :param user_email: the user's email
    :return: user
    """
    user = session.query(db.User).filter(user_email == db.User.email).first()
    return add_user(user_email) if user is None else user

def add_user(user_email):
    """
    adding a user to the database
    :param user_email: the user's email
    :return: the user's id
    """
    # Create a new User object
    user = db.User(email=user_email)
    session.add(user)
    session.commit()
    return session.query(db.User).filter_by(email=user_email).first()

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

def upload_file(uid, filename, upload_time, finish_time, status, user_id=0):
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
    if user_id != 0:
        user = session.query(db.User).filter_by(id=user_id).first()
        file = db.Upload(uid=uid, filename=filename, upload_time=upload_time, finish_time=finish_time, status=status,
                         user_id=user_id, user=user)
    else:
        file = db.Upload(uid=uid, filename=filename, upload_time=upload_time, finish_time=finish_time, status=status,
                         user_id=user_id)

    session.add(file)
    session.commit()

def get_upload_by_uid(uid):
    """
    getting an upload file by uid
    :param uid: file's uid
    :return: the upload file
    """
    uid_as_uuid = uuid.UUID(uid)
    return session.query(db.Upload).filter(db.Upload.uid == uid_as_uuid).first()

def get_upload_by_filename_email(filename, email):
    user = get_user(email)
    filename_without_extension = filename[:-5]
    return session.query(db.Upload).join(db.User).filter(
        db.Upload.user_id == user.id,
        db.Upload.filename == filename_without_extension).order_by(asc(db.Upload.upload_time)).first()

def delete_file(uid):
    """
    delete the file from the database using the uid
    :param uid: file's uid
    """
    file = session.query(db.Upload).filter_by(uid=uid).first()
    if file:
        session.delete(file)
        session.commit()

def get_pending():
    """
     Retrieve all pending uploads from the database.
    :return: List of db.Upload objects representing pending uploads.
    """
    return session.query(db.Upload).filter(db.Upload.status == 'pending').all()

def peoccessed_by_explainer(uid, finish_time):
    """
    update the data in the database and changes the status to done
    :param uid:
    :param finish_time:
    :return:
    """
    upload = session.query(db.Upload).filter_by(uid=uid).first()
    upload.status = 'done'
    upload.finish_time = finish_time
    session.commit()
