import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from janlp import utils
from janlp.models import Token, TokenLookupResult, TokenQuery, TokenWithMeanings

app = FastAPI()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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
            lemma=token.lemma,
            pron_lemma=token.pron_lemma,
            pos=token.pos,
            surface=token.surface,
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail="Word not found in dictionary")


@app.post("/analyze", response_model=list[TokenWithMeanings])
def fetch_glossary(input: SentenceInput):
    logger.debug(f"To analyze {input.sentence}")
    try:
        return utils.get_glossary(input.sentence, input.exclude_pos)
    except Exception as e:
        logger.error(e)


@app.on_event("startup")
async def startup_event():
    """Tagger has a startup cost (loading dict etc.), so run once at the very beginning."""
    utils.init_tagger()
    utils.init_jamdict()
