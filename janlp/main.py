from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from janlp import utils
from janlp.models import Token

app = FastAPI()


class SentenceInput(BaseModel):
    sentence: str


@app.post("/tokenize", response_model=list[Token])
def fetch_tokens(input: SentenceInput):
    sentence = input.sentence
    return utils.tokenize(sentence)


@app.post("/lookup", response_model=Token)
def fetch_lookup_result(token: Token):
    try:
        return utils.lookup_word(
            lemma=token.lemma, pron_lemma=token.pron_lemma, pos=token.pos
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Word not found in dictionary")


@app.post("/analyze", response_model=list[Token])
def fetch_analysis(input: SentenceInput):
    tokens = fetch_tokens(input)
    for token in tokens:
        lr = fetch_lookup_result(token)
        token.meanings = lr.meanings

    return tokens
