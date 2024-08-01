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
    "surface": "いえ",
    "dictionary_form": "いえ",
    "part_of_speech": "INTJ",
    "grammar_point": null
  },
  {
    "surface": "、",
    "dictionary_form": "、",
    "part_of_speech": "PUNCT",
    "grammar_point": null
  },
  {
    "surface": "錯覚",
    "dictionary_form": "錯覚",
    "part_of_speech": "NOUN",
    "grammar_point": null
  },
 ...
  {
    "surface": "ん",
    "dictionary_form": "ぬ",
    "part_of_speech": "AUX",
    "grammar_point": null
  },
  {
    "surface": "。",
    "dictionary_form": "。",
    "part_of_speech": "PUNCT",
    "grammar_point": null
  }
]
```

### `POST /lookup`

Return meaning of a Japanese word in English. E.g., payload

```json
{
  "word": "ある"
}
```

leads to

```json
{
  "word": "ある",
  "meanings": [
    {
      "lang": "eng",
      "gend": "",
      "text": "to be"
    },
    {
      "lang": "eng",
      "gend": "",
      "text": "to exist"
    },
	...
  ]
}
```

## Docker

Use Tsinghua mirror: `docker build --build-arg LOC=CN -t janlp .`, otherwise ignore the `--buid-arg LOC=CN` part.

Start the service with `docker run -p YOUR_PORT janlp`, then check `localhost:YOUR_PORT/docs`.
