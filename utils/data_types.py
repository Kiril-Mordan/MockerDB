
# types
from pydantic import BaseModel
from typing import List, Optional, Dict, Any


# define datatypes
class Item(BaseModel):
    text: str

class InitializeParams(BaseModel):
    embedder_params: Optional[Dict[str, Any]] = None
    database_name: Optional[str] = None

class InsertItem(BaseModel):
    data: List[Dict[str, Any]]  # List of dictionaries to support various data structures
    var_for_embedding_name: str  # Variable name to be used for embedding
    embed: Optional[bool] = True  # Whether to embed the data
    database_name: Optional[str] = None

class SearchRequest(BaseModel):
    query: str
    database_name: Optional[str] = None
    search_results_n: Optional[int] = None
    filter_criteria: Optional[Dict[str, Any]] = None
    similarity_search_type: Optional[str] = None
    similarity_params: Optional[Dict[str, Any]] = None
    perform_similarity_search: Optional[bool] = None
    return_keys_list: Optional[List[str]] = None

class DeleteItem(BaseModel):
    filter_criteria: Dict[str, str]
    database_name: Optional[str] = None

class UpdateItem(BaseModel):
    filter_criteria: Dict[str, str]
    update_values: Dict[str, str]
    database_name: Optional[str] = None

class EmbeddingRequest(BaseModel):
    texts: List[str]
    embedding_model: Optional[str]

class RemoveHandlersRequest(BaseModel):
    handler_names: List[str]