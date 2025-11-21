from typing import Dict, Any, Optional, List
import logging
import typesense
import json

# /home/joseph/code/lishana/scripts/typesense.py
# Skeleton Typesense client for a local Typesense server.
# Replace api_key and adjust settings as needed.


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class TypesenseClient:
    """
    Lightweight wrapper around the typesense python client for local dev.
    Use create_collection(schema) to create collections from a schema dict.
    """

    def __init__(
        self,
        api_key: str = "xyz",  # replace with your API key or load from env/secret manager
        host: str = "localhost",
        port: int = 8108,
        protocol: str = "http",
        connection_timeout_seconds: int = 2,
    ):
        self.config = {
            "api_key": api_key,
            "nodes": [{"host": host, "port": port, "protocol": protocol}],
            "connection_timeout_seconds": connection_timeout_seconds,
        }
        self._client: Optional[typesense.Client] = None

    @property
    def client(self) -> typesense.Client:
        """Lazily instantiate and return the typesense client."""
        if self._client is None:
            self._client = typesense.Client(self.config)
        return self._client

    @property
    def collections(self):  # proxy to allow client.collections[...] usage
        return self.client.collections

    def get_collections(self) -> List[Dict[str, Any]]:
        """Return list of existing collections."""
        try:
            return self.client.collections.retrieve()
        except Exception as exc:
            logger.exception("Failed to retrieve collections: %s", exc)
            raise

    def collection_exists(self, name: str) -> bool:
        try:
            self.client.collections[name].retrieve()
            return True
        except typesense.exceptions.ObjectNotFound:
            return False
        except Exception:
            # re-raise for unexpected errors
            raise

    def create_collection(self, schema: Dict[str, Any], overwrite: bool = False) -> Dict[str, Any]:
        """
        Create a collection from a Typesense schema dict.

        schema example:
        {
            "name": "books",
            "fields": [
                {"name": "id", "type": "string"},
                {"name": "title", "type": "string"},
                {"name": "authors", "type": "string[]", "facet": False},
            ],
            "default_sorting_field": "publication_year"
        }
        """
        name = schema.get("name")
        if not name:
            raise ValueError("Schema must include a 'name' field")

        if self.collection_exists(name):
            if overwrite:
                logger.info("Deleting existing collection %s (overwrite=True)", name)
                self.delete_collection(name)
            else:
                logger.info("Collection %s already exists; skipping creation", name)
                return self.client.collections[name].retrieve()

        try:
            created = self.client.collections.create(schema)
            logger.info("Created collection %s", name)
            return created
        except Exception as exc:
            logger.exception("Failed to create collection %s: %s", name, exc)
            raise

    def delete_collection(self, name: str) -> Dict[str, Any]:
        """Delete a collection by name."""
        try:
            return self.client.collections[name].delete()
        except Exception as exc:
            logger.exception("Failed to delete collection %s: %s", name, exc)
            raise

    def ensure_collections(self, schemas: List[Dict[str, Any]], overwrite: bool = False) -> None:
        """Ensure a set of schemas exist as collections (create if missing)."""
        for schema in schemas:
            self.create_collection(schema, overwrite=overwrite)


if __name__ == "__main__":
    # Quick local example usage. Replace API key before running.
    client = TypesenseClient(api_key="<YOUR_API_KEY>", host="localhost", port=8108, protocol="http")

    # Schema for Assyrian dictionary collection (add required 'id' field)
    assyrian_schema = {
        "name": "assyrian_dictionary",
        "fields": [
            {"name": "id", "type": "string"},  # unique id (word+pos)
            {"name": "word", "type": "string"},
            {"name": "lang_code", "type": "string", "facet": True},
            {"name": "pos", "type": "string", "facet": True},
            {"name": "forms", "type": "string[]"},  # list of surface forms
            {"name": "romanizations", "type": "string[]"},  # extracted romanization forms
            {"name": "glosses", "type": "string[]"},  # glosses aggregated from senses
            {"name": "categories", "type": "string[]", "facet": True},
            {"name": "senses_count", "type": "int32"},  # number of senses for optional sorting
        ],
        "default_sorting_field": "senses_count",
    }

    # Create collection if missing
    # client.ensure_collections([assyrian_schema], overwrite=False)

    # # Import documents from kaikki JSONL
    # import json, os
    # src_path = os.path.join(os.path.dirname(__file__), 'data', 'kaikki.org-dictionary-AssyrianNeoAramaic.jsonl')
    # coll = client.client.collections['assyrian_dictionary'].documents

    # def transform(rec: dict) -> dict:
    #     forms = []
    #     romans = []
    #     for f in rec.get('forms', []):
    #         form = f.get('form')
    #         if form:
    #             forms.append(form)
    #         if 'roman' in f:
    #             romans.append(f['roman'])
    #         if 'romanization' in f.get('tags', []):
    #             forms.append(f.get('form'))  # already added; harmless
    #     # also some romanization entries use form itself (tags include romanization)
    #     romans.extend([f.get('form') for f in rec.get('forms', []) if 'romanization' in f.get('tags', [])])
    #     # dedupe
    #     forms = list(dict.fromkeys([x for x in forms if x]))
    #     romans = list(dict.fromkeys([x for x in romans if x]))
    #     glosses = []
    #     categories = []
    #     for s in rec.get('senses', []):
    #         glosses.extend(s.get('glosses') or s.get('raw_glosses') or [])
    #         for c in s.get('categories', []):
    #             nm = c.get('name')
    #             if nm:
    #                 categories.append(nm)
    #     glosses = list(dict.fromkeys(glosses))
    #     categories = list(dict.fromkeys(categories))
    #     return {
    #         'id': f"{rec.get('word','')}_{rec.get('pos','')}",
    #         'word': rec.get('word',''),
    #         'lang_code': rec.get('lang_code',''),
    #         'pos': rec.get('pos',''),
    #         'forms': forms,
    #         'romanizations': romans,
    #         'glosses': glosses,
    #         'categories': categories,
    #         'senses_count': len(rec.get('senses', [])),
    #     }

    # batch = []
    # batch_size = 500
    # imported = 0
    # with open(src_path, 'r', encoding='utf-8') as fh:
    #     for line in fh:
    #         line = line.strip()
    #         if not line:
    #             continue
    #         try:
    #             rec = json.loads(line)
    #         except Exception:
    #             continue  # skip malformed lines
    #         doc = transform(rec)
    #         batch.append(doc)
    #         if len(batch) >= batch_size:
    #             payload = '\n'.join(json.dumps(b, ensure_ascii=False) for b in batch)
    #             coll.import_(payload, {'action': 'upsert'})
    #             imported += len(batch)
    #             batch.clear()
    # if batch:
    #     payload = '\n'.join(json.dumps(b, ensure_ascii=False) for b in batch)
    #     coll.import_(payload, {'action': 'upsert'})
    #     imported += len(batch)
    # logger.info("Imported %d documents into assyrian_dictionary", imported)

    res = client.collections['assyrian_dictionary'].documents.search({
        'q': 'ܟܠܒܐ',
        'query_by': 'glosses, word, forms, romanizations',
        'filter_by': 'pos:=[noun]',
        'per_page': 5,
    })
    print(json.dumps(res, ensure_ascii=False, indent=2))