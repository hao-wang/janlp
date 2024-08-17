from pydantic import BaseModel


class Token(BaseModel):
    surface: str
    lemma: str
    pron_lemma: str
    pron: str | None = None
    pos: str | None = None
    pos_ja: str | None = None


class TokenWithMeanings(Token):
    meanings: list[str] | None = None


class TokenQuery(BaseModel):
    lemma: str
    surface: str | None = None
    pron_lemma: str | None = None
    pos: str | None = None


class TokenLookupResult(BaseModel):
    meanings: list[str] | None = None
