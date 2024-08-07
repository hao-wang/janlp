from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from janlp import utils
from janlp.models import Token, TokenLookupResult, TokenQuery

app = FastAPI()


class SentenceInput(BaseModel):
    sentence: str
    exclude_pos: list[str] | None = None


@app.post("/tokenize", response_model=list[Token])
def fetch_tokens(input: SentenceInput):
    sentence = input.sentence
    return utils.tokenize(sentence)


@app.post("/lookup", response_model=TokenLookupResult)
def fetch_lookup_result(token: TokenQuery):
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

    # for token in tokens:
    #    query = TokenQuery(
    #        lemma=token.lemma, pron_lemma=token.pron_lemma, pos=token.pos
    #    )
    #    res = fetch_lookup_result(query)

    return tokens


@app.on_event("startup")
async def startup_event():
    utils.init_tagger()
