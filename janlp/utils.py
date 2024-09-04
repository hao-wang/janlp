import logging
from pathlib import Path

import fugashi
import jaconv
import unidic
from jamdict import Jamdict

from janlp.models import Token, TokenLookupResult, TokenWithMeanings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# TODO: jam.lookup() may give char's meaning if the word is not found. Deal with that.
jam = None
dic_dir = Path.cwd() / "dicdir"
if dic_dir.exists():
    unidic.DICDIR = dic_dir
tagger = None


def init_tagger():
    "Run once when service starts"
    global tagger
    tagger = fugashi.Tagger()


def init_jamdict():
    global jam
    jam = Jamdict()


def tokenize(sentence: str) -> list[Token]:
    """Fugashi splits the sentence into token. Pronunciations are in *Katakana*."""
    pos_mapping = {
        "名詞": "noun",
        "動詞": "verb",
        "形容詞": "adjective",
        "副詞": "adverb",
        "連体詞": "pre-noun adjectival (rentaishi)",
        "助詞": "particle",
        "助動詞": "auxiliary",
        "接続詞": "conjunction",
        "感動詞": "interjection",
        "記号": "symbol",
        "接頭詞": "prefix",
        "接頭辞": "prefix",
        "接尾詞": "suffix",
        "接尾辞": "suffix",
        "代名詞": "pronoun",
        "数詞": "numeral",
        "補助記号": "symbol",
    }
    result = tagger(sentence)
    tokens = [
        Token(
            surface=res.surface,
            pos_ja=res.feature.pos1,
            pos=pos_mapping.get(res.feature.pos1, ""),
            pron=res.feature.pron,
            lemma=res.feature.lemma,
            pron_lemma=res.feature.pronBase,
        )
        for res in result
    ]
    return tokens


def lookup_word(
    *,
    lemma: str | None = None,
    surface: str | None = None,
    pron_lemma: str | None = None,
    pos: str | None = None,
) -> TokenLookupResult:
    """Given a Japanese lemma, it's pronunciation (in Katagana) and part-of-speech
    (mapped to English & Romaji), look up it's meanings.

    1. Search with lemma if it's not None;
    2. Otherwise, search with surface(including numbers);
    3. Jamdict's words' pronunciations are in Hiragana, DIFFERS from Fugashi's tokens

    TODO: look up for わたし returns many with other prons, filter them.
    """
    # pre-process
    if lemma:
        lemma = lemma.split("-")[0]
    if pron_lemma:
        pron_lemma = jaconv.kata2hira(pron_lemma)

    result = None
    if lemma:
        result = jam.lookup(lemma)
    elif surface:
        result = jam.lookup(surface)

    meanings = []
    if result is None:
        return TokenLookupResult(meanings=[])

    for idx, entry in enumerate(result.entries):
        logger.debug(f"{idx}: {entry.kanji_forms}, {entry.kana_forms}")
        for sense in entry.senses:
            kanji_forms = [k.text for k in entry.kanji_forms]
            reading_forms = [r.text for r in entry.kana_forms]
            pos_str = ", ".join([spe.lower() for spe in sense.pos])

            # Check if the gloss matches the criteria
            # 1. (lemma in kanji_forms, or pron_lemma in reading_forms) and
            # 2. pos string contained in any element of sense.pos(list)
            if (
                (
                    (lemma is None)
                    or (lemma in kanji_forms)  # kanji
                    or (lemma in reading_forms)  # hiragana
                )
                or (
                    (pron_lemma is None)
                    or pron_lemma in reading_forms  # normalized to hiragana
                )
            ) and ((pos is None) or (pos in pos_str)):
                meanings.extend([str(sg) for sg in sense.gloss])

    return TokenLookupResult(meanings=sorted(set(meanings)))


def get_glossary(
    sentence: str,
    exclude_pos: list[str] | None = None,
) -> list[TokenWithMeanings]:
    glossary = []
    if exclude_pos is None:
        exclude_pos = [
            "auxiliary",
            "particle",
            "symbol",
        ]

    logger.debug(f"Analyzing {sentence}, add meanings(excluding {exclude_pos})")
    tokens = tokenize(sentence)

    for token in tokens:
        logger.debug(f"Token dict: {token}")
        token_wm = TokenWithMeanings(**token.__dict__)
        if (
            exclude_pos is None
            or token.pos not in exclude_pos
            and ((token.lemma and token.lemma.strip()) or token.surface)
        ):
            result = lookup_word(
                lemma=token.lemma,
                pron_lemma=token.pron_lemma,
                pos=token.pos,
                surface=token.surface,
            )
            logger.debug(f"Lookup result: {result}")
            token_wm.meanings = result.meanings

        glossary.append(token_wm)
    return glossary


def is_kanji(char):
    # Check if the character is within the Unicode ranges for Kanji
    return (
        "\u4e00" <= char <= "\u9fbf"
        or "\u3400" <= char <= "\u4dbf"
        or "\uf900" <= char <= "\ufaff"
    )


def is_hiragana(char):
    # Check if the character is within the Unicode range for Hiragana
    return "\u3040" <= char <= "\u309f"


def is_katakana(char):
    # Check if the character is within the Unicode range for Katakana
    return "\u30a0" <= char <= "\u30ff" or "\u31f0" <= char <= "\u31ff"
