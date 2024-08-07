from pathlib import Path

import fugashi
import unidic
from jamdict import Jamdict

from janlp.models import Token, TokenLookupResult

# TODO: jam.lookup() may give char's meaning if the word is not found. Deal with that.
jam = Jamdict()
# Tagger has a startup cost (loading dict etc.), so run once at the very beginning.
unidic.DICDIR = Path(__file__).parent.parent / "dicdir"
tagger = None


def init_tagger():
    "Run once when service starts"
    global tagger
    tagger = fugashi.Tagger()


def tokenize(sentence: str) -> list[Token]:
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
        "接尾詞": "suffix",
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
    lemma: str,
    pron_lemma: str,
    pos: str | None = None,
) -> TokenLookupResult:
    """Given a Japanese lemma, it's pronunciation (in Katagana or Hiragana) and part-of-speech
    (mapped to English & Romaji), look up it's meanings.


    TODO: look up for わたし returns many with other prons, filter them.
    """
    # Why not lookup(lemma)? 'Cause Unidic lemma for カナダ would be カナダ-canada
    result = jam.lookup(lemma)

    if not result.entries:
        print("No entries for lemma")
        result = jam.lookup(pron_lemma)

    meanings = []
    for idx, entry in enumerate(result.entries):
        for sense in entry.senses:
            kanji_forms = [k.text for k in entry.kanji_forms]
            reading_forms = [r.text for r in entry.kana_forms]
            pos_str = ", ".join([spe.lower() for spe in sense.pos])

            # Check if the gloss matches the criteria
            # 1. lemma in kanji_forms or pron_lemma in reading_forms, and
            # 2. pos string contained in any element of sense.pos(list)
            if (
                (
                    (lemma is None)  # desired lemma not given
                    or (lemma in kanji_forms)  # 汉字
                    or (lemma in reading_forms)  # 平假名
                )
                or (
                    (pron_lemma is None) or pron_lemma in reading_forms  # 片假名
                )
            ) and ((pos is None) or (pos in pos_str)):
                meanings.extend([str(sg) for sg in sense.gloss])

    return TokenLookupResult(meanings=sorted(set(meanings)))


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
