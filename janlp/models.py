from pydantic import BaseModel


class Token(BaseModel):
    lemma: str
    surface: str | None = None
    pos: str | None = None
    pron_lemma: str | None = None
    pron: str | None = None
    pos_ja: str | None = None
    meanings: list[str] | None = None
