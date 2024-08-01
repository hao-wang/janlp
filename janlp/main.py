from fastapi import FastAPI, HTTPException
from janlp.models import SentenceInput, TokenInfo, DictionaryLookup
from janlp import utils

app = FastAPI()

@app.post("/tokenize", response_model=list[TokenInfo])
async def tokenize(input: SentenceInput):
    result = utils.tokenize_japanese(input.sentence)
    print([res['surface'] for res in result])
    return result

@app.post("/lookup")
async def lookup(input: DictionaryLookup):
    meanings = utils.lookup_word(input.word)
    if meanings:
        return {"word": input.word, "meanings": meanings}
    else:
        raise HTTPException(status_code=404, detail="Word not found in dictionary")

@app.get("/")
async def root():
    return {"message": "Welcome to the Japanese Tokenizer and Dictionary API"}

@app.on_event("startup")
async def startup_event():
    # Load it once at the start of the service, and use the instance in the memory.
    utils.load_spacy_model()