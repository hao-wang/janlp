from pydantic import BaseModel


class Token(BaseModel):
    surface: str
    lemma: str
    pron_lemma: str
    pron: str | None = None
    pos: str | None = None
    pos_ja: str | None = None


class TokenQuery(BaseModel):
    lemma: str
    pron_lemma: str
    pos: str | None = None


class TokenLookupResult(BaseModel):
    meanings: list[str] | None = None
