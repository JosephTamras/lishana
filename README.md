# [Lishana](https://lishana.vercel.app/) - Assyrian-English Dictionary
Lishana is an Assyrian-English dictionary powered by [Typesense](https://github.com/typesense/typesense) -- a free, open-source search engine backend. Assyrian ([Suret](https://en.wikipedia.org/wiki/Suret_language)) is a very low-resource semitic language that descends from Old Aramaic. The goal of this project is to produce an even better search engine for the relatively small corpus of terms (~6,000 entries) that exist in the [Kaikki](https://kaikki.org/) machine readable dictionary. 

## Features
- Full-text Search: Search in English or Syriac with built-in typo tolerance.

- Flexible Querying: Search by glosses, canonical forms, inflected forms, or transliterations.

- Semantic Search: Vector-based search using embeddings of the glosses.

- Hybrid Search: Fuses lexical and semantic results.
    - This ensures that even if a query doesn't strictly match a dictionary entry, the engine can retrieve conceptually similar results.

- Reactive UI: Built with InstantSearch.js for a fast, app-like experience.

## Setup
1. In order to set this up locally, you will first need to set up a Typesense server. The easiest way to do this is to follow the [instructions](https://typesense.org/docs/guide/install-typesense.html) in Typesense's documentation. 

2. Please download the [Kaikki data for Assyrian](https://kaikki.org/dictionary/Assyrian%20Neo-Aramaic/index.html) and save it to `./scripts/data`. Also, be sure to 

```bash
pip install typesense
```
3. Index the data by running,
```bash
python scripts/typesense_helper.py
```
This script adds to the Kaikki data by isolating a field for the canonical form of the word as well as its phonetic transliteration which the AIITranslit.py script provides us.

4. A `.env.local` file must be created with the following environement variables
```
NEXT_PUBLIC_TYPESENSE_URL=http://localhost:8108
NEXT_PUBLIC_TYPESENSE_API_KEY=<YOUR_TYPESENSE_API_KEY>
NEXT_PUBLIC_TYPESENSE_COLLECTION_NAME=assyrian_dictionary
```

Note: The api_key defaults to `xyz`

5. Now, all you need to do is run 

```bash
npm run dev
```

and your dev server should start at `localhost:3000`. Now just type in the searchbox a query in English or Syriac!