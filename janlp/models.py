from pydantic import BaseModel

class SentenceInput(BaseModel):
    sentence: str

class TokenInfo(BaseModel):
    surface: str
    dictionary_form: str
    part_of_speech: str
    grammar_point: str | None

class DictionaryLookup(BaseModel):
    word: str