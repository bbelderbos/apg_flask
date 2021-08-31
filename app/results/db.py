import os
from datetime import datetime
from typing import Optional

from sqlmodel import create_engine, Session, SQLModel, select
from dotenv import load_dotenv

from .models import File

load_dotenv()

engine = create_engine(os.environ["DATABASE_URL"])


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def show_files():
    with Session(engine) as session:
        return session.exec(select(File))


def upsert_file(
    phrase_file_name: str,
    sound_file_name: str,
    attenuation: int
) -> File:
    with Session(engine) as session:
        statement = select(File).where(
            File.phrase_file_name == phrase_file_name,
            File.sound_file_name == sound_file_name
        )
        results = session.exec(statement)
        file = results.first()

        if file is not None:
            file.updated = datetime.now()
        else:
            file = File(
                phrase_file_name=phrase_file_name,
                sound_file_name=sound_file_name,
                attenuation=attenuation,
                added=datetime.now(),
                updated=datetime.now())

        session.add(file)
        session.commit()
        session.refresh(file)
        return file


def update_file_with_result(
    file_id: int,
    phrase_file_path: str,
    sound_file_path: str,
    result_file_path: Optional[str] = None,
    exception: Optional[str] = None,
):
    with Session(engine) as session:
        file = session.get(File, file_id)
        file.phrase_file_path = phrase_file_path
        file.sound_file_path = sound_file_path
        file.result_file_path = result_file_path
        file.exception = exception
        file.updated = datetime.now()  # TODO: can model do this automatically?
        session.add(file)
        session.commit()
        session.refresh(file)
        return file
