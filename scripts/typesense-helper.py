from typing import Dict, Any, Optional, List
import logging
import typesense
import json
import os
import argparse
from pathlib import Path
from AIITranslit import AIITranslit

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
        name = schema.get("name")
        if not name:
            raise ValueError("Schema must include a 'name' field")

        if self.collection_exists(name):
            if overwrite:
                logger.info(
                    "Deleting existing collection %s (overwrite=True)", name)
                self.delete_collection(name)
            else:
                logger.info(
                    "Collection %s already exists; skipping creation", name)
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

class AssyrianSchema:
    def __init__(self):
        self.schema = {
            "name": "assyrian_dictionary",
            "enable_nested_fields": True,
            "fields": [
                {"name": "pos", "type": "string"},
                {"name": "forms.form", "type": "string[]"},
                {"name": "forms.roman", "type": "string[]", "optional": True},
                {"name": "word", "type": "string"},
                {"name": "senses.glosses", "type": "string[]"},
                {"name": "forms.phonetic", "type": "string[]", "optional": True},
                {
                    "name": "glosses_embedding",
                    "type": "float[]",
                    "embed": {
                        "from": [
                            "senses.glosses"
                        ],
                        "model_config": {
                            "model_name": "ts/all-MiniLM-L12-v2"
                        }
                    }
                }
            ]
        }

    @staticmethod
    def transform_record(record: Dict[str, Any]) -> Dict[str, Any]:
        """Transform kaikki record to include the phonetic field in each form of the entry"""
        for form in record.get("forms", []):
            word = form.get("form", "")
            if word:
                form["phonetic"] = AIITranslit(word)['phonetic']
        
        return record



def _load_dotenv_from_repo_root(dotenv_filename: str = ".env") -> None:
    """Load simple KEY=VALUE pairs from a .env file at the repository root into os.environ.

    This avoids adding an external dependency; it only sets variables that are not
    already present in the environment.
    """
    repo_root = Path(__file__).resolve().parents[1]
    dotenv_path = repo_root / dotenv_filename
    if not dotenv_path.exists():
        return
    try:
        for raw in dotenv_path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip()
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            if key and key not in os.environ:
                os.environ[key] = val
    except Exception:
        # Don't fail loudly for this convenience loader; fall back to environment only.
        pass


def update_collection(client: TypesenseClient, schema: dict) -> None:
    """Import documents from kaikki JSONL into the Typesense collection."""
    src_path = os.path.join(os.path.dirname(
        __file__), 'data', 'kaikki.org-dictionary-AssyrianNeoAramaic.jsonl')
    coll = client.client.collections[schema["name"]].documents

    batch = []
    batch_size = 500
    imported = 0
    with open(src_path, 'r', encoding='utf-8') as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                print(f"Skipping malformed line: {line[:30]}...")
                continue  # skip malformed lines
            

            batch.append(AssyrianSchema.transform_record(rec))
            if len(batch) >= batch_size:
                payload = '\n'.join(json.dumps(b, ensure_ascii=False)
                                    for b in batch)
                result = coll.import_(payload, {'action': 'upsert'})
                if '400' in result:
                    print("Import result:", result)
                imported += len(batch)
                batch.clear()
    if batch:
        payload = '\n'.join(json.dumps(b, ensure_ascii=False) for b in batch)
        result = coll.import_(payload, {'action': 'upsert'})
        # print if success is in result string
        if '400' in result:
            print("Import result:", result)
        imported += len(batch)
    logger.info("Imported %d documents into assyrian_dictionary", imported)


def test_query(client: TypesenseClient) -> None:
    """Run an example search query against the collection."""
    res = client.client.collections['assyrian_dictionary'].documents.search({
        'q': 'ܟܠܒܐ',
        'query_by': 'senses.glosses',
        'filter_by': 'pos:=[noun]',
        'per_page': 5,
    })
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Typesense helper script for Assyrian dictionary management"
    )
    parser.add_argument(
        "action",
        choices=["update", "test"],
        help="Action to perform: 'update' to import documents, 'test' to run example query"
    )
    args = parser.parse_args()

    _load_dotenv_from_repo_root()

    api_key = os.getenv("TYPESENSE_API_KEY", "xyz")
    client = TypesenseClient(
        api_key=api_key, host="localhost", port=8108, protocol="http"
        )

    # Schema for Assyrian dictionary collection (add required 'id' field)
    assyrian_schema = AssyrianSchema().schema

    # Create collection if missing
    client.ensure_collections([assyrian_schema], overwrite=True)

    if args.action == "update":
        update_collection(client, assyrian_schema)
    elif args.action == "test":
        test_query(client)
