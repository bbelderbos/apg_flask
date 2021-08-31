from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class File(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    phrase_file_name: str
    sound_file_name: str
    attenuation: int
    added: datetime
    updated: datetime
    phrase_file_path: Optional[str] = None
    sound_file_path: Optional[str] = None
    result_file_path: Optional[str] = None
    exception: Optional[str] = None
