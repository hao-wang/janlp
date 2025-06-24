import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from janlp import utils
from janlp.models import Token, TokenLookupResult, TokenQuery, TokenWithMeanings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup: Initialize tagger and jamdict
    logger.info("Initializing tagger and setting jamdict path...")
    utils.init_tagger()
    utils.init_jamdict_path()  # Set global DB path, connections will be thread-local
    logger.info("Initialization complete.")
    
    yield
    
    # Shutdown: cleanup if needed
    logger.info("Application shutting down.")


app = FastAPI(lifespan=lifespan)


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
        raise HTTPException(status_code=500, detail="Internal server error")
