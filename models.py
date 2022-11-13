from pydantic import BaseModel
from pathlib import Path

class Replace(BaseModel):
    search_string: str
    replace_string: str
    save: bool | None = None
    save_path: Path | None = None