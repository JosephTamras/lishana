from typing import Dict, Any, Optional, List
import logging
import typesense

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
    client = TypesenseClient(api_key="xyz", host="localhost", port=8108, protocol="http")

    # Example schema to create a collection called "books"
    examples = [
        {
            "name": "books",
            "fields": [
                {"name": "id", "type": "string"},
                {"name": "title", "type": "string"},
                {"name": "authors", "type": "string[]"},
                {"name": "publication_year", "type": "int32", "facet": False},
            ],
            "default_sorting_field": "publication_year",
        }
    ]

    # Create collections if missing
    client.ensure_collections(examples, overwrite=False)