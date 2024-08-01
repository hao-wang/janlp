import spacy
from jamdict import Jamdict


jam = Jamdict()
nlp = None

def load_spacy_model():
    global nlp
    nlp = spacy.load("ja_ginza_electra")

def tokenize_japanese(sentence):
    doc = nlp(sentence)
    result = []
    for token in doc:
        word_info = {
            'surface': token.text,
            'dictionary_form': token.lemma_,
            'part_of_speech': token.pos_,
            'grammar_point': None
        }
        result.append(word_info)
    return result

def lookup_word(word):
    result = jam.lookup(word)
    
    if result.entries:
        meanings = []
        for entry in result.entries:
            for sense in entry.senses:
                meanings.extend(sense.gloss)
        return meanings
    else:
        return None