# Japanese NLP

## Features

FastAPI backed services:

### `POST /tokenize`:

Split a Japanese sentence into tokens. E.g., with payload

```json
{
  "sentence": "いえ、錯覚ではありません。"
}
```

we get

```json
[
  {
    "lemma": "言う",
    "surface": "いえ",
    "pos": "verb",
    "pron_lemma": "イエル",
    "pron": "イエ",
    "pos_ja": "動詞",
    "meanings": null
  },
  {
    "lemma": "、",
    "surface": "、",
    "pos": "",
    "pron_lemma": "*",
    "pron": "*",
    "pos_ja": "補助記号",
    "meanings": null
  },
  {
    "lemma": "錯覚",
    "surface": "錯覚",
    "pos": "noun",
    "pron_lemma": "サッカク",
    "pron": "サッカク",
    "pos_ja": "名詞",
    "meanings": null
  },
  {
    "lemma": "で",
    "surface": "で",
    "pos": "particle",
    "pron_lemma": "デ",
    "pron": "デ",
    "pos_ja": "助詞",
    "meanings": null
  },
  {
    "lemma": "は",
    "surface": "は",
    "pos": "particle",
    "pron_lemma": "ワ",
    "pron": "ワ",
    "pos_ja": "助詞",
    "meanings": null
  },
  {
    "lemma": "有る",
    "surface": "あり",
    "pos": "verb",
    "pron_lemma": "アル",
    "pron": "アリ",
    "pos_ja": "動詞",
    "meanings": null
  },
  {
    "lemma": "ます",
    "surface": "ませ",
    "pos": "auxiliary",
    "pron_lemma": "マス",
    "pron": "マセ",
    "pos_ja": "助動詞",
    "meanings": null
  },
  {
    "lemma": "ず",
    "surface": "ん",
    "pos": "auxiliary",
    "pron_lemma": "ヌ",
    "pron": "ン",
    "pos_ja": "助動詞",
    "meanings": null
  },
  {
    "lemma": "。",
    "surface": "。",
    "pos": "",
    "pron_lemma": "*",
    "pron": "*",
    "pos_ja": "補助記号",
    "meanings": null
  }
]
```

### `POST /lookup`

Return meaning of a Japanese word in English. E.g., payload

```json
{
  "lemma": "ある",
  "pos": "verb"
}
```

leads to

```json
{
  "lemma": "ある",
  "surface": null,
  "pos": "verb",
  "pron_lemma": null,
  "pron": null,
  "pos_ja": null,
  "meanings": [
    "to be",
    "to be equipped with",
    "to be located",
    "to come about",
    "to exist",
    "to happen",
    "to have",
    "to live"
  ]
}
```

## Docker

1. Get the image: `docker pull hosdce/janlp:latest`
1. Start the service: e.g., `docker run janlp`
