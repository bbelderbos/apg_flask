import os

from dotenv import load_dotenv

from app import app
from app.celery import make_celery
from app.aws import create_audio_mix as _create_audio_mix
from app.results.db import (create_db_and_tables,
                            upsert_file,
                            update_file_with_result)

load_dotenv()

app.config.update(
    CELERY_BROKER_URL=os.environ["CELERY_BROKER_URL"],
)
celery = make_celery(app)
create_db_and_tables()


@celery.task()
def create_audio_mix(
    req_phrase_filename,
    req_phrase_file_content_encoded,
    req_sound_filename,
    req_sound_file_content_encoded,
    **kwargs
):
    # keep state in db
    file = upsert_file(
        req_phrase_filename, req_sound_filename, kwargs.get("attenuation", 10)
    )

    # this takes long
    phrase_file_path, sound_file_path, result_file_path, exception = (
        _create_audio_mix(
            req_phrase_filename,
            req_phrase_file_content_encoded,
            req_sound_filename,
            req_sound_file_content_encoded,
            **kwargs
        )
    )

    # update db with results
    update_file_with_result(
        file.id, phrase_file_path, sound_file_path, result_file_path, exception
    )
